"""
AI Market Insights - Sentiment Analytics Engine
Two scheduled functions for real-time sentiment gauge and daily analytics
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import functions_v2

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Firebase
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app()
db = firestore.client()

# Ticker to Sector Mapping
TICKER_TO_SECTOR = {
    # IT Sector
    "TCS": "IT",
    "INFY": "IT", 
    "WIPRO": "IT",
    "HCLTECH": "IT",
    "TECHM": "IT",
    "MINDTREE": "IT",
    "LTI": "IT",
    "MPHASIS": "IT",
    
    # Banking Sector
    "HDFCBANK": "Banking",
    "ICICIBANK": "Banking",
    "KOTAKBANK": "Banking",
    "SBIN": "Banking",
    "AXISBANK": "Banking",
    "INDUSINDBK": "Banking",
    "BANDHANBNK": "Banking",
    "FEDERALBNK": "Banking",
    
    # Pharma Sector
    "SUNPHARMA": "Pharma",
    "DRREDDY": "Pharma",
    "CIPLA": "Pharma",
    "BIOCON": "Pharma",
    "DIVISLAB": "Pharma",
    "LUPIN": "Pharma",
    "AUROPHARMA": "Pharma",
    "CADILAHC": "Pharma",
    
    # Auto Sector
    "MARUTI": "Auto",
    "TATAMOTORS": "Auto",
    "M&M": "Auto",
    "BAJAJ-AUTO": "Auto",
    "HEROMOTOCO": "Auto",
    "EICHERMOT": "Auto",
    "ASHOKLEY": "Auto",
    "TVSMOTORS": "Auto",
    
    # FMCG Sector
    "HINDUNILVR": "FMCG",
    "ITC": "FMCG",
    "NESTLEIND": "FMCG",
    "DABUR": "FMCG",
    "BRITANNIA": "FMCG",
    "GODREJCP": "FMCG",
    "MARICO": "FMCG",
    "COLPAL": "FMCG",
    
    # Energy Sector
    "RELIANCE": "Energy",
    "ONGC": "Energy",
    "GAIL": "Energy",
    "BPCL": "Energy",
    "HPCL": "Energy",
    "IOC": "Energy",
    "PETRONET": "Energy",
    "ADANIGREEN": "Energy",
    
    # Metals Sector
    "TATASTEEL": "Metals",
    "JSWSTEEL": "Metals",
    "HINDALCO": "Metals",
    "SAIL": "Metals",
    "JINDALSTEL": "Metals",
    "VEDL": "Metals",
    "NMDC": "Metals",
    "COALINDIA": "Metals",
    
    # Real Estate Sector
    "DLF": "Real Estate",
    "GODREJPROP": "Real Estate",
    "BRIGADE": "Real Estate",
    "SOBHA": "Real Estate",
    "MAHLIFE": "Real Estate",
    "PURAVANKARA": "Real Estate",
    "SUNTECK": "Real Estate",
    "LODHA": "Real Estate",
    
    # Telecom Sector
    "BHARTIARTL": "Telecom",
    "RCOM": "Telecom",
    "TATACOMM": "Telecom",
    "IDEA": "Telecom",
    
    # Power Sector
    "NTPC": "Power",
    "POWERGRID": "Power",
    "TATAPOWER": "Power",
    "ADANIPOWER": "Power",
    "TORNTPOWER": "Power",
    "CESC": "Power",
    "RPOWER": "Power",
    "SUZLON": "Power"
}

# Sector list for initialization
SECTORS = [
    "IT", "Banking", "Pharma", "Auto", "FMCG", 
    "Energy", "Metals", "Real Estate", "Telecom", "Power"
]


class SentimentAnalytics:
    """Main class for sentiment analytics calculations"""
    
    def __init__(self):
        self.db = db
    
    def _sentiment_to_score(self, sentiment: str) -> int:
        """Convert sentiment string to numerical score"""
        sentiment_lower = sentiment.lower()
        if sentiment_lower == "positive":
            return 1
        elif sentiment_lower == "negative":
            return -1
        else:  # neutral or unknown
            return 0
    
    def _get_articles_in_timeframe(self, start_time: datetime, end_time: datetime) -> List[Dict[str, Any]]:
        """Query articles within a specific timeframe"""
        try:
            articles_ref = self.db.collection('articles')
            query = articles_ref.where('publishedAt', '>=', start_time).where('publishedAt', '<=', end_time)
            
            docs = query.stream()
            articles = []
            
            for doc in docs:
                article_data = doc.to_dict()
                article_data['id'] = doc.id
                articles.append(article_data)
            
            logger.info(f"Retrieved {len(articles)} articles from {start_time} to {end_time}")
            return articles
            
        except Exception as e:
            logger.error(f"Error querying articles: {str(e)}")
            return []
    
    def calculate_real_time_sentiment(self) -> Dict[str, Any]:
        """
        Function 1: Calculate real-time sentiment for the gauge
        Returns average sentiment score for last 6 hours
        """
        try:
            logger.info("Starting real-time sentiment calculation...")
            
            # Calculate 6-hour rolling window
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=6)
            
            # Query articles in the timeframe
            articles = self._get_articles_in_timeframe(start_time, end_time)
            
            if not articles:
                logger.warning("No articles found in 6-hour window, defaulting to neutral")
                return {
                    "averageScore": 0.0,
                    "lastUpdated": firestore.SERVER_TIMESTAMP,
                    "articlesAnalyzed": 0,
                    "timeWindow": "6 hours"
                }
            
            # Calculate sentiment scores
            sentiment_scores = []
            for article in articles:
                sentiment = article.get('sentiment', 'Neutral')
                score = self._sentiment_to_score(sentiment)
                sentiment_scores.append(score)
            
            # Calculate average
            average_score = sum(sentiment_scores) / len(sentiment_scores)
            
            result = {
                "averageScore": round(average_score, 3),
                "lastUpdated": firestore.SERVER_TIMESTAMP,
                "articlesAnalyzed": len(articles),
                "timeWindow": "6 hours"
            }
            
            logger.info(f"Real-time sentiment calculated: {average_score:.3f} from {len(articles)} articles")
            return result
            
        except Exception as e:
            logger.error(f"Error calculating real-time sentiment: {str(e)}")
            return {
                "averageScore": 0.0,
                "lastUpdated": firestore.SERVER_TIMESTAMP,
                "articlesAnalyzed": 0,
                "timeWindow": "6 hours",
                "error": str(e)
            }
    
    def calculate_daily_analytics(self, target_date: str = None) -> Dict[str, Any]:
        """
        Function 2: Calculate daily analytics for historical charts
        Returns comprehensive daily sentiment breakdown
        """
        try:
            logger.info(f"Starting daily analytics calculation for {target_date or 'today'}...")
            
            # Determine target date
            if target_date:
                target_datetime = datetime.strptime(target_date, "%Y-%m-%d")
            else:
                target_datetime = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Calculate day boundaries
            start_time = target_datetime
            end_time = start_time + timedelta(days=1)
            
            # Query articles for the entire day
            articles = self._get_articles_in_timeframe(start_time, end_time)
            
            if not articles:
                logger.warning(f"No articles found for {target_date}, creating empty record")
                return self._create_empty_daily_record(target_date or target_datetime.strftime("%Y-%m-%d"))
            
            # Initialize sector tracking
            sector_scores = defaultdict(list)
            overall_scores = []
            
            # Process each article
            for article in articles:
                sentiment = article.get('sentiment', 'Neutral')
                score = self._sentiment_to_score(sentiment)
                overall_scores.append(score)
                
                # Process tickers for sector analysis
                tickers = article.get('tickers', [])
                for ticker in tickers:
                    ticker_upper = ticker.upper()
                    if ticker_upper in TICKER_TO_SECTOR:
                        sector = TICKER_TO_SECTOR[ticker_upper]
                        sector_scores[sector].append(score)
            
            # Calculate overall sentiment
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
                "articlesAnalyzed": len(articles),
                "sectorBreakdown": sector_breakdown,
                "lastUpdated": firestore.SERVER_TIMESTAMP,
                "processingTime": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Daily analytics calculated: {overall_sentiment:.3f} from {len(articles)} articles")
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
    
    def save_real_time_sentiment(self, sentiment_data: Dict[str, Any]) -> bool:
        """Save real-time sentiment to market_status collection"""
        try:
            doc_ref = self.db.collection('market_status').document('current_sentiment')
            doc_ref.set(sentiment_data)
            
            logger.info("Real-time sentiment saved to market_status/current_sentiment")
            return True
            
        except Exception as e:
            logger.error(f"Error saving real-time sentiment: {str(e)}")
            return False
    
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
analytics = SentimentAnalytics()


def real_time_sentiment_gauge(request):
    """
    Cloud Function 1: Real-time Sentiment Gauge Engine
    Triggered every 15 minutes (offset by 5 minutes from Phase 1)
    """
    logger.info("Starting real-time sentiment gauge calculation...")
    
    try:
        # Calculate real-time sentiment
        sentiment_data = analytics.calculate_real_time_sentiment()
        
        # Save to Firestore
        success = analytics.save_real_time_sentiment(sentiment_data)
        
        if success:
            logger.info("Real-time sentiment gauge updated successfully")
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Real-time sentiment updated',
                    'data': sentiment_data
                })
            }
        else:
            logger.error("Failed to save real-time sentiment")
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Failed to save sentiment data'})
            }
            
    except Exception as e:
        logger.error(f"Error in real-time sentiment gauge: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


def daily_analytics_engine(request):
    """
    Cloud Function 2: Daily Analytics Engine
    Triggered daily at 11:55 PM
    """
    logger.info("Starting daily analytics calculation...")
    
    try:
        # Calculate daily analytics
        analytics_data = analytics.calculate_daily_analytics()
        
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
    # Test real-time sentiment
    print("Testing real-time sentiment calculation...")
    sentiment_data = analytics.calculate_real_time_sentiment()
    print(f"Real-time sentiment: {sentiment_data}")
    
    # Test daily analytics
    print("\nTesting daily analytics calculation...")
    analytics_data = analytics.calculate_daily_analytics()
    print(f"Daily analytics: {analytics_data}")
