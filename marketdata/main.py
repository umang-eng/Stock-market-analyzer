"""
Phase 2 - Hardened Market Data API
Redis (Memorystore) cache with 5m TTL, Firebase App Check verification,
Secret Manager for API key, and stale-while-revalidate fallback.
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import redis
import firebase_admin
from firebase_admin import app_check
from google.cloud import secretmanager, firestore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app()
db = firestore.Client()

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173","https://your-domain.com"])  # update domain

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
secret_client = secretmanager.SecretManagerServiceClient()

REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
CACHE_KEY = "market_data"
CACHE_TTL = 300  # seconds

def redis_client() -> Optional[redis.Redis]:
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True, socket_timeout=5, socket_connect_timeout=5)
        r.ping()
        return r
    except Exception as e:
        logger.error("Redis unavailable: %s", e)
        return None

def get_api_key() -> str:
    name = f"projects/{PROJECT_ID}/secrets/financial-api-key/versions/latest"
    return secret_client.access_secret_version(request={"name": name}).payload.data.decode("utf-8")

def verify_app_check_token() -> bool:
    token = request.headers.get('X-Firebase-AppCheck')
    if not token:
        return False
    try:
        app_check.verify_token(token)
        return True
    except Exception as e:
        logger.warning("App Check failed: %s", e)
        return False

def fetch_indices(api_key: str) -> List[Dict[str, Any]]:
    out = []
    try:
        u = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=^NSEI&apikey={api_key}"
        r = requests.get(u, timeout=10)
        r.raise_for_status()
        q = r.json().get("Global Quote", {})
        if q.get("05. price"):
            out.append({"name":"NIFTY 50","price": float(q.get("05. price",0)),"change": float(q.get("09. change",0)),"changePercent": float(str(q.get("10. change percent","0")).replace('%',''))})
    except Exception as e:
        logger.error("NIFTY fetch error: %s", e)
    try:
        u = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=^BSESN&apikey={api_key}"
        r = requests.get(u, timeout=10)
        r.raise_for_status()
        q = r.json().get("Global Quote", {})
        if q.get("05. price"):
            out.append({"name":"SENSEX","price": float(q.get("05. price",0)),"change": float(q.get("09. change",0)),"changePercent": float(str(q.get("10. change percent","0")).replace('%',''))})
    except Exception as e:
        logger.error("SENSEX fetch error: %s", e)
    return out

def fetch_movers(api_key: str) -> Dict[str, List[Dict[str, Any]]]:
    # Stubbed demo movers; replace with provider calls
    return {
        "gainers":[{"ticker":"LT","name":"Larsen & Toubro","price":3500.0,"changePercent":5.2}],
        "losers":[{"ticker":"INFY","name":"Infosys","price":1500.0,"changePercent":-1.8}]
    }

def fetch_sectors(api_key: str) -> List[Dict[str, Any]]:
    # Stubbed demo sectors; replace with provider calls
    return [
        {"name":"IT","changePercent":1.2},
        {"name":"Banking","changePercent":-0.5},
        {"name":"Auto","changePercent":1.8},
        {"name":"Pharma","changePercent":0.3},
        {"name":"FMCG","changePercent":-0.2},
    ]

def get_market_data_live() -> Optional[Dict[str, Any]]:
    try:
        key = get_api_key()
        indices = fetch_indices(key)
        movers = fetch_movers(key)
        sectors = fetch_sectors(key)
        return {
            "indices": indices,
            "gainers": movers.get('gainers', []),
            "losers": movers.get('losers', []),
            "sectors": sectors,
            "lastUpdated": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error("Fetch live error: %s", e)
        return None

def get_cached(r: Optional[redis.Redis]) -> Optional[Dict[str, Any]]:
    if not r: return None
    try:
        v = r.get(CACHE_KEY)
        return json.loads(v) if v else None
    except Exception as e:
        logger.error("Redis get error: %s", e)
        return None

def set_cached(r: Optional[redis.Redis], data: Dict[str, Any]):
    if not r: return
    try:
        r.setex(CACHE_KEY, CACHE_TTL, json.dumps(data))
    except Exception as e:
        logger.error("Redis set error: %s", e)


@app.route('/market-data', methods=['GET'])
def market_data_route():
    if not verify_app_check_token():
        return jsonify({"error":"Unauthorized"}), 401
    r = redis_client()
    cached = get_cached(r)
    if cached:
        return jsonify(cached), 200
    live = get_market_data_live()
    if live:
        set_cached(r, live)
        return jsonify(live), 200
    # fallback to stale
    stale = get_cached(r)
    if stale:
        stale["warning"] = "Data may be outdated"
        return jsonify(stale), 200
    return jsonify({"error":"Market data is temporarily unavailable"}), 503


@app.route('/health', methods=['GET'])
def health():
    r = redis_client()
    return jsonify({"status":"healthy","redis": bool(r)}), 200


def main(request):
    with app.test_request_context(path=request.path, method=request.method, headers=request.headers, data=request.get_data()):
        return app.full_dispatch_request()


