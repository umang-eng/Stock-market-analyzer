"""
AI Research API - Professional Market Intelligence for Indian Stocks
HTTP Cloud Function (Gen2, Python 3.12) secured via CORS and Secret Manager.
Uses Gemini with Google Search grounding to produce structured, citeable market research.
"""

import json
import logging
import os
from datetime import datetime
from typing import Any, Dict

from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from google.cloud import secretmanager

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)
CORS(app, origins=[
  "http://localhost:5173",
  "https://your-domain.com"
])

# Secrets
secret_client = secretmanager.SecretManagerServiceClient()
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")


def _get_gemini_api_key() -> str:
  secret_name = f"projects/{PROJECT_ID}/secrets/gemini-api-key/versions/latest"
  resp = secret_client.access_secret_version(request={"name": secret_name})
  return resp.payload.data.decode("utf-8")


def _init_model():
  api_key = _get_gemini_api_key()
  genai.configure(api_key=api_key)
  model = genai.GenerativeModel(
    "gemini-2.0-flash-exp",
    tools=[{"google_search": {}}]
  )
  return model


def _build_prompt(question: str) -> str:
  return f"""
ROLE: You are a professional Indian equity market research analyst.
AUDIENCE: Sophisticated investors and financial professionals.
SCOPE: Use Google Search grounding to find the latest credible news, filings, and data from top Indian sources.
SOURCES: moneycontrol.com, economictimes.indiatimes.com, livemint.com, business-standard.com, nseindia.com, sebi.gov.in, bseindia.com.
GEOGRAPHY: India markets only.

TASK: Analyze the following market research query and produce a concise, executive-grade brief with citations.
QUERY: "{question}"

OUTPUT: Return ONLY a valid JSON object with the exact shape below:
{{
  "executiveSummary": "2-4 sentence overview with clear conclusion",
  "keyFindings": [
    {{ "title": "finding title", "detail": "1-3 sentence detail", "impact": "Positive|Negative|Neutral" }}
  ],
  "relatedTickers": ["RELIANCE", "TCS"],
  "sectors": ["IT", "Banking"],
  "riskFactors": ["key risk 1", "key risk 2"],
  "sources": [
    {{ "name": "Moneycontrol", "url": "https://..." }}
  ],
  "timestamp": "ISO8601"
}}

REQUIREMENTS:
- Use Google Search grounding and prefer authoritative Indian sources.
- Use exact ticker symbols in UPPERCASE if mentioned; otherwise omit.
- Limit keyFindings to 3-6 high-signal items; include impact.
- Include at least 3 credible sources with direct URLs.
- Keep strictly to the JSON format. No markdown, no prose outside JSON.
"""


@app.route("/ai/research", methods=["POST"])  
def ai_research_http():
  try:
    payload = request.get_json(silent=True) or {}
    question = (payload.get("question") or "").strip()
    if not question:
      return jsonify({"error": "Missing 'question'"}), 400

    model = _init_model()

    prompt = _build_prompt(question)
    resp = model.generate_content(
      prompt,
      generation_config={
        "temperature": 0.2,
        "max_output_tokens": 4096,
        "response_mime_type": "application/json"
      }
    )

    # Parse JSON
    data = json.loads(resp.text)

    # Minimal sanitation
    data.setdefault("timestamp", datetime.utcnow().isoformat())
    data.setdefault("keyFindings", [])
    data.setdefault("sources", [])
    data.setdefault("relatedTickers", [])
    data.setdefault("sectors", [])
    data.setdefault("riskFactors", [])

    return jsonify(data), 200
  except json.JSONDecodeError:
    logger.exception("AI returned malformed JSON")
    return jsonify({"error": "AI response malformed"}), 502
  except Exception as e:
    logger.exception("AI research error")
    return jsonify({"error": str(e)}), 500


def ai_research_function(request):
  with app.test_request_context(
    path=request.path,
    method=request.method,
    headers=request.headers,
    data=request.get_data()
  ):
    return app.full_dispatch_request()
