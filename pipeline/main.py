"""
Phase 1 - Hardened News Pipeline with Integrated Real-time Sentiment
Single-call Gemini (search + analysis), Pydantic validation, dedupe via set(),
and 6h rolling sentiment update to market_status/current_sentiment.
"""

import json
import logging
import os
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Set

import firebase_admin
from firebase_admin import firestore
from google.cloud import secretmanager
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential
from pydantic import BaseModel, Field, validator
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app()
db = firestore.client()

secret_client = secretmanager.SecretManagerServiceClient()


class SentimentEnum(str, Enum):
    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    NEUTRAL = "Neutral"


class ArticleModel(BaseModel):
    headline: str = Field(..., min_length=1, max_length=500)
    source: str = Field(..., min_length=1, max_length=100)
    url: str = Field(..., regex=r'^https?://.+')
    summary: str = Field(..., min_length=10, max_length=1000)
    sentiment: SentimentEnum
    tickers: List[str] = Field(default_factory=list, max_items=20)
    sectors: List[str] = Field(default_factory=list, max_items=10)

    @validator('tickers')
    def v_tickers(cls, v):
        return [t.upper().strip() for t in v if t and isinstance(t, str)]

    @validator('sectors')
    def v_sectors(cls, v):
        valid = {"IT","Banking","Pharma","Auto","FMCG","Energy","Metals","Real Estate","Telecom","Power"}
        return list({s.strip() for s in v if isinstance(s, str) and s.strip() in valid})


class ArticleListModel(BaseModel):
    articles: List[ArticleModel] = Field(default_factory=list, max_items=50)


class Pipeline:
    NEWS_SOURCES = [
        "site:moneycontrol.com",
        "site:economictimes.indiatimes.com",
        "site:livemint.com",
        "site:business-standard.com",
        "site:financialexpress.com",
        "site:thehindubusinessline.com",
        "site:nseindia.com",
        "site:bseindia.com",
        "site:sebi.gov.in",
    ]

    def __init__(self):
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT not set")
        self.model = self._init_model()
        self.existing_urls: Set[str] = set()

    def _init_model(self):
        api_key_name = f"projects/{self.project_id}/secrets/gemini-api-key/versions/latest"
        api_key = secret_client.access_secret_version(request={"name": api_key_name}).payload.data.decode("utf-8")
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-2.0-flash-exp", tools=[{"google_search": {}}])

    def _combined_prompt(self) -> str:
        sources = " OR ".join([f'"{s}"' for s in self.NEWS_SOURCES])
        return f"""
TASK: In one operation, search and analyze latest Indian stock market news.
SOURCES: {sources}
WINDOW: last 15-20 minutes. Output ONLY JSON with:
{{
  "articles": [{{
    "headline": "...",
    "source": "...",
    "url": "https://...",
    "summary": "1-2 sentence impact summary",
    "sentiment": "Positive"|"Negative"|"Neutral",
    "tickers": ["RELIANCE","TCS"],
    "sectors": ["IT","Banking"]
  }}]
}}
STRICT: No markdown, no prose outside JSON. Tickers uppercase, sectors from [IT,Banking,Pharma,Auto,FMCG,Energy,Metals,Real Estate,Telecom,Power]. Max 30 articles.
"""

    def _load_existing_urls(self):
        cutoff = datetime.utcnow() - timedelta(hours=24)
        q = db.collection('articles').where('publishedAt', '>=', cutoff).select(['url'])
        self.existing_urls = {d.to_dict().get('url') for d in q.stream() if d.to_dict().get('url')}

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    def fetch_and_analyze(self) -> List[Dict[str, Any]]:
        prompt = self._combined_prompt()
        resp = self.model.generate_content(prompt, generation_config={
            "temperature": 0.2,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json"
        })
        text = (resp.text or "").strip()
        # Strip markdown fences if any
        m = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
        if m:
            text = m.group(1)
        data = json.loads(text)
        validated = ArticleListModel(**data)
        return [a.dict() for a in validated.articles]

    def _filter_new(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        out = []
        for a in articles:
            url = a.get('url')
            if url and url not in self.existing_urls:
                out.append(a)
        return out

    def _batch_save(self, articles: List[Dict[str, Any]]) -> int:
        if not articles:
            return 0
        batch = db.batch()
        ref = db.collection('articles')
        count = 0
        for a in articles:
            doc = ref.document()
            payload = {**a, "publishedAt": firestore.SERVER_TIMESTAMP, "processedAt": firestore.SERVER_TIMESTAMP}
            batch.set(doc, payload)
            count += 1
        batch.commit()
        return count

    def _sentiment_to_score(self, s: str) -> int:
        s = (s or '').lower()
        if s == 'positive':
            return 1
        if s == 'negative':
            return -1
        return 0

    def update_realtime_sentiment(self) -> Dict[str, Any]:
        end = datetime.utcnow()
        start = end - timedelta(hours=6)
        q = db.collection('articles').where('publishedAt', '>=', start).where('publishedAt', '<=', end)
        scores = []
        total = 0
        for d in q.stream():
            total += 1
            scores.append(self._sentiment_to_score(d.to_dict().get('sentiment', 'Neutral')))
        avg = sum(scores) / len(scores) if scores else 0.0
        doc = db.collection('market_status').document('current_sentiment')
        payload = {
            "averageScore": round(avg, 3),
            "lastUpdated": firestore.SERVER_TIMESTAMP,
            "articlesAnalyzed": total,
            "timeWindow": "6 hours"
        }
        doc.set(payload)
        return payload

    def run(self) -> Dict[str, Any]:
        stats = {"fetched": 0, "new_articles": 0, "saved": 0, "errors": 0}
        try:
            self._load_existing_urls()
            articles = self.fetch_and_analyze()
            stats["fetched"] = len(articles)
            new_articles = self._filter_new(articles)
            stats["new_articles"] = len(new_articles)
            stats["saved"] = self._batch_save(new_articles)
            self.update_realtime_sentiment()
            return stats
        except Exception as e:
            logger.exception("Pipeline error")
            stats["errors"] += 1
            return stats


def main(request):
    p = Pipeline()
    stats = p.run()
    return {"statusCode": 200, "body": json.dumps(stats)}


