# AI Market Insights - News Pipeline

## Overview
Serverless Google Cloud Function that automatically fetches, analyzes, and stores Indian stock market news articles.

## Features
- 🔍 Automatic article discovery using Google Search grounding
- 🤖 AI-powered sentiment analysis with Gemini
- 💾 Firebase Firestore integration for storage
- 🔄 Duplicate detection and prevention
- ⏰ Automated scheduling (every 15 minutes)
- 🛡️ Robust error handling and retries

## Setup Instructions

### Prerequisites
1. Google Cloud Project with billing enabled
2. Firebase project set up
3. Gemini API key
4. Google Cloud SDK installed

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
- Set `GEMINI_API_KEY` in environment variables
- Configure Firebase credentials (service account JSON)

### 3. Deploy to Cloud Function
```bash
./deploy.sh
```

Or manually:
```bash
gcloud functions deploy news-pipeline \
  --gen2 \
  --runtime=python312 \
  --region=asia-south1 \
  --source=. \
  --entry-point=news_pipeline \
  --trigger-http \
  --allow-unauthenticated \
  --timeout=540s \
  --memory=1GB
```

### 4. Create Cloud Scheduler Job
```bash
gcloud scheduler jobs create http news-pipeline-scheduler \
  --location=asia-south1 \
  --schedule="*/15 * * * *" \
  --uri="https://asia-south1-your-project.cloudfunctions.net/news-pipeline" \
  --http-method=POST \
  --time-zone="Asia/Kolkata"
```

## Configuration

### News Sources
Edit `NEWS_SOURCES` in `main.py` to add/remove sources:
```python
NEWS_SOURCES = [
    "site:moneycontrol.com",
    "site:economictimes.indiatimes.com",
    # Add more sources here
]
```

### Analysis Schema
The AI analysis returns:
- `headline`: Article headline
- `source`: News source name
- `url`: Article URL
- `summary`: AI-generated summary
- `sentiment`: Positive/Negative/Neutral
- `tickers`: Array of stock tickers (e.g., ["RELIANCE", "TCS"])

## Monitoring
View logs in Google Cloud Console:
```bash
gcloud functions logs read news-pipeline --gen2 --region=asia-south1
```

## Cost Estimation
- Cloud Function: ~$0.40 per million invocations
- Gemini API: Pay-as-you-go for tokens
- Firestore: Free tier includes 50K reads/day

## Security Notes
- Store API keys in Secret Manager (production)
- Use IAM roles for least privilege
- Enable VPC connector if needed

## Troubleshooting
1. Check logs for errors
2. Verify API keys are set
3. Ensure Firestore is properly initialized
4. Check function timeout settings

## Local Testing
```bash
python main.py
```

## Support
For issues, check Cloud Logging or contact the development team.
