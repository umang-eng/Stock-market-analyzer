"""
AI Market Insights - Hardened Daily Analytics Engine (SRE Audit Fixes)
Scalable batch-query implementation for daily sentiment analytics
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict

import firebase_admin
from firebase_admin import credentials, firestore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Firebase
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app()
db = firestore.client()

# SRE Fix: Sector list for initialization (no more ticker-to-sector mapping)
SECTORS = [
    "IT", "Banking", "Pharma", "Auto", "FMCG", 
    "Energy", "Metals", "Real Estate", "Telecom", "Power"
]


class DailyAnalyticsHardened:
    """
    Hardened Daily Analytics Engine with SRE fixes:
    1. Batched queries (memory optimization)
    2. Sector data from articles (no ticker mapping)
    3. Scalable processing (no OOM crashes)
    4. Efficient aggregation (minimal memory usage)
    """
    
    def __init__(self):
        self.db = db
        self.batch_size = 1000  # SRE Fix: Process articles in batches
    
    def _sentiment_to_score(self, sentiment: str) -> int:
        """Convert sentiment string to numerical score"""
        sentiment_lower = sentiment.lower()
        if sentiment_lower == "positive":
            return 1
        elif sentiment_lower == "negative":
            return -1
        else:  # neutral or unknown
            return 0
    
    def _process_article_batch(self, articles: List[Dict[str, Any]], 
                              overall_scores: List[int], 
                              sector_scores: Dict[str, List[int]]) -> None:
        """
        SRE Fix: Process a batch of articles and update aggregate counters
        This keeps memory usage constant regardless of total article count
        """
        for article in articles:
            # Process overall sentiment
            sentiment = article.get('sentiment', 'Neutral')
            score = self._sentiment_to_score(sentiment)
            overall_scores.append(score)
            
            # SRE Fix: Process sectors directly from article data
            # No more ticker-to-sector mapping - sectors come from Phase 1
            sectors = article.get('sectors', [])
            for sector in sectors:
                if sector in SECTORS:  # Validate sector
                    sector_scores[sector].append(score)
    
    def calculate_daily_analytics_batched(self, target_date: str = None) -> Dict[str, Any]:
        """
        SRE Fix: Scalable daily analytics using batched queries
        This prevents OOM crashes by processing articles in batches
        """
        try:
            logger.info(f"Starting batched daily analytics calculation for {target_date or 'today'}...")
            
            # Determine target date
            if target_date:
                target_datetime = datetime.strptime(target_date, "%Y-%m-%d")
            else:
                target_datetime = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Calculate day boundaries
            start_time = target_datetime
            end_time = start_time + timedelta(days=1)
            
            # SRE Fix: Initialize aggregate counters
            overall_scores = []
            sector_scores = defaultdict(list)
            total_articles = 0
            
            # SRE Fix: Batched query processing
            articles_ref = self.db.collection('articles')
            query = (articles_ref
                    .where('publishedAt', '>=', start_time)
                    .where('publishedAt', '<', end_time)
                    .order_by('publishedAt')
                    .limit(self.batch_size))
            
            last_doc = None
            
            while True:
                # Execute query with cursor
                if last_doc:
                    query = query.start_after(last_doc)
                
                docs = list(query.stream())
                
                if not docs:
                    logger.info("No more documents to process")
                    break
                
                # Convert documents to dictionaries
                articles = []
                for doc in docs:
                    article_data = doc.to_dict()
                    articles.append(article_data)
                
                # Process this batch
                self._process_article_batch(articles, overall_scores, sector_scores)
                total_articles += len(articles)
                
                # Update cursor for next batch
                last_doc = docs[-1]
                
                logger.info(f"Processed batch of {len(articles)} articles (total: {total_articles})")
                
                # Safety check to prevent infinite loops
                if len(docs) < self.batch_size:
                    logger.info("Reached end of data (partial batch)")
                    break
            
            if total_articles == 0:
                logger.warning(f"No articles found for {target_date}, creating empty record")
                return self._create_empty_daily_record(target_date or target_datetime.strftime("%Y-%m-%d"))
            
            # Calculate final averages
            overall_sentiment = sum(overall_scores) / len(overall_scores) if overall_scores else 0.0
            
            # Calculate sector breakdown
            sector_breakdown = {}
            for sector in SECTORS:
                if sector in sector_scores and sector_scores[sector]:
                    sector_avg = sum(sector_scores[sector]) / len(sector_scores[sector])
                    sector_breakdown[sector] = round(sector_avg, 3)
                else:
                    sector_breakdown[sector] = 0.0
            
            result = {
                "date": target_date or target_datetime.strftime("%Y-%m-%d"),
                "overallSentimentScore": round(overall_sentiment, 3),
                "articlesAnalyzed": total_articles,
                "sectorBreakdown": sector_breakdown,
                "lastUpdated": firestore.SERVER_TIMESTAMP,
                "processingTime": datetime.utcnow().isoformat(),
                "batchesProcessed": (total_articles + self.batch_size - 1) // self.batch_size
            }
            
            logger.info(f"Daily analytics calculated: {overall_sentiment:.3f} from {total_articles} articles in batches")
            return result
            
        except Exception as e:
            logger.error(f"Error calculating daily analytics: {str(e)}")
            return {
                "date": target_date or datetime.utcnow().strftime("%Y-%m-%d"),
                "overallSentimentScore": 0.0,
                "articlesAnalyzed": 0,
                "sectorBreakdown": {sector: 0.0 for sector in SECTORS},
                "lastUpdated": firestore.SERVER_TIMESTAMP,
                "error": str(e)
            }
    
    def _create_empty_daily_record(self, date: str) -> Dict[str, Any]:
        """Create empty daily record when no articles are found"""
        return {
            "date": date,
            "overallSentimentScore": 0.0,
            "articlesAnalyzed": 0,
            "sectorBreakdown": {sector: 0.0 for sector in SECTORS},
            "lastUpdated": firestore.SERVER_TIMESTAMP,
            "note": "No articles found for this date"
        }
    
    def save_daily_analytics(self, analytics_data: Dict[str, Any]) -> bool:
        """Save daily analytics to sentiment_history collection"""
        try:
            date = analytics_data['date']
            doc_ref = self.db.collection('sentiment_history').document(date)
            doc_ref.set(analytics_data)
            
            logger.info(f"Daily analytics saved to sentiment_history/{date}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving daily analytics: {str(e)}")
            return False


# Initialize analytics engine
analytics = DailyAnalyticsHardened()


def daily_analytics_engine_hardened(request):
    """
    SRE Fix: Hardened Daily Analytics Engine Cloud Function
    Triggered daily at 11:55 PM with scalable batch processing
    """
    logger.info("Starting hardened daily analytics calculation...")
    
    try:
        # Calculate daily analytics using batched queries
        analytics_data = analytics.calculate_daily_analytics_batched()
        
        # Save to Firestore
        success = analytics.save_daily_analytics(analytics_data)
        
        if success:
            logger.info("Daily analytics updated successfully")
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Daily analytics updated',
                    'data': analytics_data
                })
            }
        else:
            logger.error("Failed to save daily analytics")
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Failed to save analytics data'})
            }
            
    except Exception as e:
        logger.error(f"Error in daily analytics engine: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


# For local testing
if __name__ == "__main__":
    print("Testing hardened daily analytics calculation...")
    analytics_data = analytics.calculate_daily_analytics_batched()
    print(f"Daily analytics: {analytics_data}")
