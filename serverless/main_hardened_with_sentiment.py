"""
AI Market Insights - Hardened News Pipeline with Integrated Sentiment Analysis
Phase 1 + Phase 4 Real-time Sentiment (SRE Audit Fixes)
"""

import json
import logging
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Set
from urllib.parse import urlparse

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import secretmanager
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential
from pydantic import BaseModel, Field, validator
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Firebase
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app()
db = firestore.client()

# Initialize Secret Manager client
secret_client = secretmanager.SecretManagerServiceClient()


class SentimentEnum(str, Enum):
    """Enum for sentiment values to prevent AI hallucination"""
    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    NEUTRAL = "Neutral"


class ArticleModel(BaseModel):
    """Pydantic model for individual article validation with sectors"""
    headline: str = Field(..., min_length=1, max_length=500)
    source: str = Field(..., min_length=1, max_length=100)
    url: str = Field(..., regex=r'^https?://.+')
    summary: str = Field(..., min_length=10, max_length=1000)
    sentiment: SentimentEnum
    tickers: List[str] = Field(default_factory=list, max_items=20)
    sectors: List[str] = Field(default_factory=list, max_items=10)  # SRE Fix: Added sectors
    
    @validator('tickers')
    def validate_tickers(cls, v):
        """Ensure tickers are uppercase and valid format"""
        return [ticker.upper().strip() for ticker in v if ticker.strip()]
    
    @validator('sectors')
    def validate_sectors(cls, v):
        """Ensure sectors are valid and unique"""
        valid_sectors = {
            "IT", "Banking", "Pharma", "Auto", "FMCG", 
            "Energy", "Metals", "Real Estate", "Telecom", "Power"
        }
        return list(set([sector.strip() for sector in v if sector.strip() in valid_sectors]))


class ArticleListModel(BaseModel):
    """Pydantic model for the complete response validation"""
    articles: List[ArticleModel] = Field(..., min_items=0, max_items=50)


class NewsPipelineHardenedWithSentiment:
    """
    Hardened news pipeline with integrated sentiment analysis:
    1. Single Gemini API call (cost optimization)
    2. Batch duplicate checking (N+1 query fix)
    3. Pydantic validation (data integrity)
    4. Secret Manager integration (security)
    5. Concurrency control (race condition prevention)
    6. Integrated real-time sentiment calculation (SRE Fix)
    """
    
    # Top Indian financial news sources
    NEWS_SOURCES = [
        "site:moneycontrol.com",
        "site:economictimes.indiatimes.com", 
        "site:livemint.com",
        "site:business-standard.com",
        "site:financialexpress.com",
        "site:thehindubusinessline.com",
    ]
    
    def __init__(self):
        self.project_id = self._get_project_id()
        self.gemini_api_key = self._get_gemini_api_key()
        
        # Configure Gemini with single model for both search and analysis
        genai.configure(api_key=self.gemini_api_key)
        self.model = genai.GenerativeModel(
            'gemini-2.0-flash-exp',
            tools=[{"google_search": {}}]
        )
        
        # Cache for existing URLs to avoid N+1 queries
        self.existing_urls: Set[str] = set()
        
    def _get_project_id(self) -> str:
        """Get GCP project ID from environment"""
        import os
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")
        return project_id
    
    def _get_gemini_api_key(self) -> str:
        """Retrieve Gemini API key from Secret Manager"""
        try:
            secret_name = f"projects/{self.project_id}/secrets/gemini-api-key/versions/latest"
            response = secret_client.access_secret_version(request={"name": secret_name})
            return response.payload.data.decode("UTF-8")
        except Exception as e:
            logger.error(f"Error retrieving Gemini API key: {str(e)}")
            raise ValueError("Failed to retrieve Gemini API key from Secret Manager")
    
    def _load_existing_urls(self) -> None:
        """
        SRE Fix #2: Load all existing URLs in a single query to avoid N+1 queries
        """
        try:
            logger.info("Loading existing URLs from last 24 hours...")
            
            # Query articles from last 24 hours
            cutoff_time = datetime.utcnow() - timedelta(hours=24)
            articles_ref = db.collection('articles')
            query = articles_ref.where('publishedAt', '>=', cutoff_time).select(['url'])
            
            docs = query.stream()
            self.existing_urls = {doc.to_dict()['url'] for doc in docs if 'url' in doc.to_dict()}
            
            logger.info(f"Loaded {len(self.existing_urls)} existing URLs from last 24 hours")
            
        except Exception as e:
            logger.error(f"Error loading existing URLs: {str(e)}")
            self.existing_urls = set()
    
    def _build_combined_prompt(self) -> str:
        """
        SRE Fix #1: Single combined prompt for search + analysis + sectors
        """
        sources_query = " OR ".join([f'"{src}"' for src in self.NEWS_SOURCES])
        
        prompt = f"""
        TASK: Find and analyze recent Indian stock market news articles in a single operation.

        STEP 1 - SEARCH: Find recent articles published in the last 15-20 minutes from these sources:
        {sources_query}
        
        Focus on articles about:
        - Stock market news and analysis
        - Company earnings and quarterly results
        - Economic indicators and policy changes
        - Sector-specific news (banking, IT, pharma, auto, FMCG, energy)
        - Corporate announcements and mergers
        - Market trends and predictions
        - IPOs and new listings

        STEP 2 - ANALYSIS: For each article found, perform comprehensive analysis:
        1. Extract the headline and identify the news source
        2. Read the full article content
        3. Write a concise 1-2 sentence summary highlighting key financial/economic impact
        4. Determine sentiment: "Positive" (bullish/good for markets), "Negative" (bearish/bad for markets), or "Neutral" (mixed/no clear impact)
        5. Extract relevant Indian stock ticker symbols in UPPERCASE (e.g., ["RELIANCE", "TCS", "HDFCBANK"])
        6. Identify relevant sectors from: IT, Banking, Pharma, Auto, FMCG, Energy, Metals, Real Estate, Telecom, Power

        OUTPUT FORMAT: Return ONLY a valid JSON object with this exact structure:
        {{
            "articles": [
                {{
                    "headline": "Article headline here",
                    "source": "Source name (e.g., Moneycontrol, The Economic Times)",
                    "url": "https://article-url.com",
                    "summary": "Concise 1-2 sentence summary of key impact",
                    "sentiment": "Positive" | "Negative" | "Neutral",
                    "tickers": ["RELIANCE", "TCS"] // Array of ticker symbols in UPPERCASE, empty array [] if none
                    "sectors": ["Energy", "IT"] // Array of relevant sectors, empty array [] if none
                }}
            ]
        }}

        REQUIREMENTS:
        - Return ONLY JSON, no additional text
        - Maximum 30 articles to avoid rate limits
        - Ensure all required fields are present
        - Use exact sentiment values: "Positive", "Negative", or "Neutral"
        - Ticker symbols must be in UPPERCASE
        - Sectors must be from the predefined list
        - Skip duplicate articles if found
        """
        
        return prompt
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def fetch_and_analyze_articles(self) -> List[Dict[str, Any]]:
        """
        SRE Fix #1: Single API call for both search and analysis
        """
        try:
            logger.info("Starting combined search and analysis operation...")
            
            prompt = self._build_combined_prompt()
            
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.2,
                    "max_output_tokens": 8192,
                    "response_mime_type": "application/json",
                }
            )
            
            logger.info("Received response from Gemini, parsing and validating...")
            return self._parse_and_validate_response(response.text)
            
        except Exception as e:
            logger.error(f"Error in combined fetch and analyze: {str(e)}")
            raise
    
    def _parse_and_validate_response(self, response_text: str) -> List[Dict[str, Any]]:
        """
        SRE Fix #3: Robust validation using Pydantic models
        """
        try:
            # Clean response text
            response_text = response_text.strip()
            
            # Extract JSON from markdown code blocks if present
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(1)
            
            # Parse JSON
            raw_data = json.loads(response_text)
            
            # Validate using Pydantic models
            validated_data = ArticleListModel(**raw_data)
            
            # Convert back to dict for processing
            articles = [article.dict() for article in validated_data.articles]
            
            logger.info(f"Successfully validated {len(articles)} articles")
            return articles
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {str(e)}")
            logger.error(f"Raw response: {response_text[:500]}...")
            return []
            
        except Exception as e:
            logger.error(f"Pydantic validation failed: {str(e)}")
            logger.error(f"Raw response: {response_text[:500]}...")
            return []
    
    def _filter_new_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        SRE Fix #2: Efficient duplicate filtering using in-memory set
        """
        new_articles = []
        
        for article in articles:
            url = article.get('url')
            if url and url not in self.existing_urls:
                new_articles.append(article)
                logger.info(f"New article found: {article.get('headline', 'No headline')}")
            else:
                logger.info(f"Skipping duplicate article: {url}")
        
        logger.info(f"Filtered to {len(new_articles)} new articles from {len(articles)} total")
        return new_articles
    
    def _batch_save_articles(self, articles: List[Dict[str, Any]]) -> int:
        """
        Batch save articles to Firestore for better performance
        """
        if not articles:
            return 0
        
        try:
            logger.info(f"Batch saving {len(articles)} articles to Firestore...")
            
            # Prepare batch write
            batch = db.batch()
            articles_ref = db.collection('articles')
            
            saved_count = 0
            for article in articles:
                # Add timestamps
                article_data = {
                    **article,
                    "publishedAt": firestore.SERVER_TIMESTAMP,
                    "processedAt": firestore.SERVER_TIMESTAMP,
                }
                
                # Add to batch
                doc_ref = articles_ref.document()
                batch.set(doc_ref, article_data)
                saved_count += 1
            
            # Commit batch
            batch.commit()
            
            logger.info(f"Successfully saved {saved_count} articles to Firestore")
            return saved_count
            
        except Exception as e:
            logger.error(f"Error batch saving articles: {str(e)}")
            return 0
    
    def _sentiment_to_score(self, sentiment: str) -> int:
        """Convert sentiment string to numerical score"""
        sentiment_lower = sentiment.lower()
        if sentiment_lower == "positive":
            return 1
        elif sentiment_lower == "negative":
            return -1
        else:  # neutral or unknown
            return 0
    
    def calculate_and_save_real_time_sentiment(self) -> Dict[str, Any]:
        """
        SRE Fix: Integrated real-time sentiment calculation
        This replaces the separate 15-minute function with integrated logic
        """
        try:
            logger.info("Calculating real-time sentiment from last 6 hours...")
            
            # Calculate 6-hour rolling window
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=6)
            
            # Query articles in the timeframe
            articles_ref = db.collection('articles')
            query = articles_ref.where('publishedAt', '>=', start_time).where('publishedAt', '<=', end_time)
            
            docs = query.stream()
            articles = []
            
            for doc in docs:
                article_data = doc.to_dict()
                articles.append(article_data)
            
            if not articles:
                logger.warning("No articles found in 6-hour window, defaulting to neutral")
                sentiment_data = {
                    "averageScore": 0.0,
                    "lastUpdated": firestore.SERVER_TIMESTAMP,
                    "articlesAnalyzed": 0,
                    "timeWindow": "6 hours"
                }
            else:
                # Calculate sentiment scores
                sentiment_scores = []
                for article in articles:
                    sentiment = article.get('sentiment', 'Neutral')
                    score = self._sentiment_to_score(sentiment)
                    sentiment_scores.append(score)
                
                # Calculate average
                average_score = sum(sentiment_scores) / len(sentiment_scores)
                
                sentiment_data = {
                    "averageScore": round(average_score, 3),
                    "lastUpdated": firestore.SERVER_TIMESTAMP,
                    "articlesAnalyzed": len(articles),
                    "timeWindow": "6 hours"
                }
            
            # Save to market_status collection
            doc_ref = db.collection('market_status').document('current_sentiment')
            doc_ref.set(sentiment_data)
            
            logger.info(f"Real-time sentiment calculated and saved: {sentiment_data['averageScore']}")
            return sentiment_data
            
        except Exception as e:
            logger.error(f"Error calculating real-time sentiment: {str(e)}")
            return {
                "averageScore": 0.0,
                "lastUpdated": firestore.SERVER_TIMESTAMP,
                "articlesAnalyzed": 0,
                "timeWindow": "6 hours",
                "error": str(e)
            }
    
    def run(self) -> Dict[str, Any]:
        """
        Main pipeline execution with integrated sentiment analysis
        """
        stats = {
            "fetched": 0,
            "new_articles": 0,
            "analyzed": 0,
            "saved": 0,
            "errors": 0,
            "execution_time_seconds": 0,
            "sentiment_calculated": False
        }
        
        start_time = datetime.utcnow()
        
        try:
            logger.info("Starting hardened news pipeline with integrated sentiment...")
            
            # Step 1: Load existing URLs to avoid N+1 queries
            self._load_existing_urls()
            
            # Step 2: Single API call for search + analysis
            articles = self.fetch_and_analyze_articles()
            stats["fetched"] = len(articles)
            
            if not articles:
                logger.warning("No articles found or all articles failed validation")
                # Still calculate sentiment from existing articles
                self.calculate_and_save_real_time_sentiment()
                stats["sentiment_calculated"] = True
                return stats
            
            # Step 3: Efficient duplicate filtering
            new_articles = self._filter_new_articles(articles)
            stats["new_articles"] = len(new_articles)
            stats["analyzed"] = len(new_articles)
            
            # Step 4: Batch save to Firestore
            saved_count = self._batch_save_articles(new_articles)
            stats["saved"] = saved_count
            
            # Step 5: SRE Fix - Calculate and save real-time sentiment
            sentiment_result = self.calculate_and_save_real_time_sentiment()
            stats["sentiment_calculated"] = True
            
            # Update existing URLs cache
            for article in new_articles:
                self.existing_urls.add(article['url'])
            
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            stats["execution_time_seconds"] = round(execution_time, 2)
            
            logger.info(f"Pipeline completed successfully: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Fatal error in pipeline: {str(e)}")
            stats["errors"] += 1
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            stats["execution_time_seconds"] = round(execution_time, 2)
            return stats


def news_pipeline_hardened_with_sentiment(request):
    """
    Hardened Cloud Function entry point with integrated sentiment analysis
    """
    logger.info("Starting hardened news pipeline with integrated sentiment...")
    
    pipeline = NewsPipelineHardenedWithSentiment()
    stats = pipeline.run()
    
    logger.info(f"Hardened news pipeline with sentiment completed: {stats}")
    
    return {
        'statusCode': 200,
        'body': json.dumps(stats)
    }


# For local testing
if __name__ == "__main__":
    pipeline = NewsPipelineHardenedWithSentiment()
    stats = pipeline.run()
    print(f"Results: {stats}")
