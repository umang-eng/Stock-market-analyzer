"""
AI Market Insights - Market Data API Proxy
Secure proxy to third-party financial data APIs with caching
"""

import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import time

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import secretmanager
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Firebase
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app()
db = firestore.client()

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:5173",  # Local development
    "https://your-domain.com",  # Production domain
])

# Cache configuration
CACHE_DURATION_MINUTES = 5
CACHE_COLLECTION = "market_data_cache"
CACHE_DOCUMENT_ID = "latest_data"


class MarketDataAPI:
    """Main class for fetching and caching market data"""
    
    def __init__(self):
        self.secret_client = secretmanager.SecretManagerServiceClient()
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        
    def _get_api_key(self) -> str:
        """Retrieve API key from Secret Manager"""
        try:
            secret_name = f"projects/{self.project_id}/secrets/financial-api-key/versions/latest"
            response = self.secret_client.access_secret_version(request={"name": secret_name})
            return response.payload.data.decode("UTF-8")
        except Exception as e:
            logger.error(f"Error retrieving API key: {str(e)}")
            # Fallback to environment variable
            return os.environ.get("FINANCIAL_API_KEY", "")
    
    def _get_cached_data(self) -> Optional[Dict[str, Any]]:
        """Retrieve cached market data from Firestore"""
        try:
            doc_ref = db.collection(CACHE_COLLECTION).document(CACHE_DOCUMENT_ID)
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                cached_at = data.get("cached_at")
                
                if cached_at:
                    # Check if cache is still valid
                    cache_time = cached_at.replace(tzinfo=None)
                    now = datetime.utcnow()
                    
                    if (now - cache_time).total_seconds() < (CACHE_DURATION_MINUTES * 60):
                        logger.info("Returning cached data")
                        return data.get("market_data")
                    else:
                        logger.info("Cache expired, will fetch new data")
                        return None
            
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving cached data: {str(e)}")
            return None
    
    def _save_cached_data(self, market_data: Dict[str, Any]) -> bool:
        """Save market data to Firestore cache"""
        try:
            doc_ref = db.collection(CACHE_COLLECTION).document(CACHE_DOCUMENT_ID)
            doc_ref.set({
                "market_data": market_data,
                "cached_at": firestore.SERVER_TIMESTAMP,
                "created_at": firestore.SERVER_TIMESTAMP
            })
            
            logger.info("Market data cached successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error saving cached data: {str(e)}")
            return False
    
    def _fetch_index_data(self, api_key: str) -> List[Dict[str, Any]]:
        """Fetch NIFTY 50 and SENSEX data"""
        indices = []
        
        # NIFTY 50 (^NSEI)
        try:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=^NSEI&apikey={api_key}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            quote = data.get("Global Quote", {})
            
            if quote:
                price = float(quote.get("05. price", 0))
                change = float(quote.get("09. change", 0))
                change_percent = float(quote.get("10. change percent", "0%").replace("%", ""))
                
                indices.append({
                    "name": "NIFTY 50",
                    "price": price,
                    "change": change,
                    "changePercent": change_percent
                })
                
        except Exception as e:
            logger.error(f"Error fetching NIFTY 50 data: {str(e)}")
        
        # SENSEX (^BSESN)
        try:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=^BSESN&apikey={api_key}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            quote = data.get("Global Quote", {})
            
            if quote:
                price = float(quote.get("05. price", 0))
                change = float(quote.get("09. change", 0))
                change_percent = float(quote.get("10. change percent", "0%").replace("%", ""))
                
                indices.append({
                    "name": "SENSEX",
                    "price": price,
                    "change": change,
                    "changePercent": change_percent
                })
                
        except Exception as e:
            logger.error(f"Error fetching SENSEX data: {str(e)}")
        
        return indices
    
    def _fetch_market_movers(self, api_key: str) -> Dict[str, List[Dict[str, Any]]]:
        """Fetch top gainers and losers"""
        gainers = []
        losers = []
        
        # Sample data - replace with actual API calls
        # In production, you would call APIs like:
        # - NSE top gainers/losers endpoint
        # - BSE top gainers/losers endpoint
        # - Or use a financial data provider
        
        try:
            # Mock data for demonstration - replace with actual API calls
            gainers = [
                {"ticker": "LT", "name": "Larsen & Toubro", "price": 3500.00, "changePercent": 5.2},
                {"ticker": "M&M", "name": "Mahindra & Mahindra", "price": 2900.00, "changePercent": 4.8},
                {"ticker": "RELIANCE", "name": "Reliance Industries", "price": 2450.00, "changePercent": 3.5},
                {"ticker": "TCS", "name": "Tata Consultancy", "price": 3200.00, "changePercent": 2.8},
                {"ticker": "HDFCBANK", "name": "HDFC Bank", "price": 1650.00, "changePercent": 2.1}
            ]
            
            losers = [
                {"ticker": "INFY", "name": "Infosys", "price": 1500.00, "changePercent": -1.8},
                {"ticker": "WIPRO", "name": "Wipro", "price": 420.00, "changePercent": -1.5},
                {"ticker": "ONGC", "name": "Oil & Natural Gas", "price": 245.00, "changePercent": -1.2},
                {"ticker": "NTPC", "name": "NTPC", "price": 265.00, "changePercent": -0.9},
                {"ticker": "COALINDIA", "name": "Coal India", "price": 385.00, "changePercent": -0.7}
            ]
            
        except Exception as e:
            logger.error(f"Error fetching market movers: {str(e)}")
        
        return {"gainers": gainers, "losers": losers}
    
    def _fetch_sector_data(self, api_key: str) -> List[Dict[str, Any]]:
        """Fetch sector performance data"""
        sectors = []
        
        try:
            # Mock data for demonstration - replace with actual sector API calls
            sectors = [
                {"name": "IT", "changePercent": 1.2},
                {"name": "Banking", "changePercent": -0.5},
                {"name": "Auto", "changePercent": 1.8},
                {"name": "Pharma", "changePercent": 0.3},
                {"name": "FMCG", "changePercent": -0.2},
                {"name": "Energy", "changePercent": 0.8},
                {"name": "Metals", "changePercent": -0.4},
                {"name": "Real Estate", "changePercent": 0.6}
            ]
            
        except Exception as e:
            logger.error(f"Error fetching sector data: {str(e)}")
        
        return sectors
    
    def fetch_fresh_data(self) -> Optional[Dict[str, Any]]:
        """Fetch fresh market data from third-party APIs"""
        try:
            api_key = self._get_api_key()
            if not api_key:
                logger.error("No API key available")
                return None
            
            logger.info("Fetching fresh market data...")
            
            # Fetch all data components
            indices = self._fetch_index_data(api_key)
            movers = self._fetch_market_movers(api_key)
            sectors = self._fetch_sector_data(api_key)
            
            # Aggregate data
            market_data = {
                "indices": indices,
                "gainers": movers["gainers"],
                "losers": movers["losers"],
                "sectors": sectors
            }
            
            logger.info("Successfully fetched fresh market data")
            return market_data
            
        except Exception as e:
            logger.error(f"Error fetching fresh data: {str(e)}")
            return None
    
    def get_market_data(self) -> Dict[str, Any]:
        """Main method to get market data (cached or fresh)"""
        # First, try to get cached data
        cached_data = self._get_cached_data()
        
        if cached_data:
            return cached_data
        
        # Cache miss or expired - fetch fresh data
        fresh_data = self.fetch_fresh_data()
        
        if fresh_data:
            # Save to cache
            self._save_cached_data(fresh_data)
            return fresh_data
        
        # If fresh data fetch failed, try to return stale cache
        logger.warning("Fresh data fetch failed, attempting to return stale cache")
        try:
            doc_ref = db.collection(CACHE_COLLECTION).document(CACHE_DOCUMENT_ID)
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                stale_data = data.get("market_data")
                if stale_data:
                    logger.info("Returning stale cached data")
                    return stale_data
        except Exception as e:
            logger.error(f"Error retrieving stale cache: {str(e)}")
        
        # Last resort - return empty data structure
        logger.error("No data available - returning empty structure")
        return {
            "indices": [],
            "gainers": [],
            "losers": [],
            "sectors": []
        }


# Initialize the API
market_api = MarketDataAPI()


@app.route('/market-data', methods=['GET'])
def get_market_data():
    """HTTP endpoint for market data"""
    try:
        # Optional: Validate Firebase App Check token
        # app_check_token = request.headers.get('X-Firebase-AppCheck')
        # if not verify_app_check_token(app_check_token):
        #     return jsonify({"error": "Invalid App Check token"}), 401
        
        # Get market data
        data = market_api.get_market_data()
        
        return jsonify(data), 200
        
    except Exception as e:
        logger.error(f"Error in market data endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()}), 200


def market_data_function(request):
    """
    Cloud Function entry point
    """
    with app.test_request_context(
        path=request.path,
        method=request.method,
        headers=request.headers,
        data=request.get_data()
    ):
        return app.full_dispatch_request()


# For local testing
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
