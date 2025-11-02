"""
Phase 4 - Hardened Daily Analytics Engine with Batched Queries
Reads sectors array on articles and aggregates sector sentiment safely.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List
from collections import defaultdict

import firebase_admin
from firebase_admin import firestore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app()
db = firestore.client()

SECTORS = ["IT","Banking","Pharma","Auto","FMCG","Energy","Metals","Real Estate","Telecom","Power"]


class DailyAnalytics:
    def __init__(self):
        self.batch_size = 1000

    def _sentiment_to_score(self, s: str) -> int:
        s = (s or '').lower()
        if s == 'positive':
            return 1
        if s == 'negative':
            return -1
        return 0

    def _process_batch(self, docs: List[Any], overall: List[int], sectors: Dict[str, List[int]]):
        for d in docs:
            data = d.to_dict()
            score = self._sentiment_to_score(data.get('sentiment', 'Neutral'))
            overall.append(score)
            for s in (data.get('sectors') or []):
                if s in SECTORS:
                    sectors[s].append(score)

    def calculate(self, date_str: str = None) -> Dict[str, Any]:
        if date_str:
            day = datetime.strptime(date_str, "%Y-%m-%d")
        else:
            day = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        start = day
        end = start + timedelta(days=1)

        overall_scores: List[int] = []
        sector_scores: Dict[str, List[int]] = defaultdict(list)
        total = 0

        ref = db.collection('articles')
        q = (ref.where('publishedAt', '>=', start)
                .where('publishedAt', '<', end)
                .order_by('publishedAt')
                .limit(self.batch_size))

        last = None
        while True:
            cur_q = q.start_after(last) if last else q
            docs = list(cur_q.stream())
            if not docs:
                break
            self._process_batch(docs, overall_scores, sector_scores)
            total += len(docs)
            last = docs[-1]
            if len(docs) < self.batch_size:
                break

        overall = (sum(overall_scores) / len(overall_scores)) if overall_scores else 0.0
        breakdown = {}
        for s in SECTORS:
            vals = sector_scores.get(s, [])
            breakdown[s] = round(sum(vals)/len(vals), 3) if vals else 0.0

        result = {
            "date": day.strftime("%Y-%m-%d"),
            "overallSentimentScore": round(overall, 3),
            "articlesAnalyzed": total,
            "sectorBreakdown": breakdown,
            "lastUpdated": firestore.SERVER_TIMESTAMP
        }
        db.collection('sentiment_history').document(result['date']).set(result)
        return result


def main(request):
    try:
        data = DailyAnalytics().calculate()
        return {"statusCode": 200, "body": json.dumps(data)}
    except Exception as e:
        logger.exception("Daily analytics error")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}


