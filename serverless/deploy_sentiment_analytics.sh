#!/bin/bash
# Deployment script for Sentiment Analytics Cloud Functions

PROJECT_ID="your-project-id"  # Replace with your GCP project ID
REGION="asia-south1"  # Mumbai region for Indian context
RUNTIME="python312"

# Set GCP project
gcloud config set project $PROJECT_ID

# Deploy Real-time Sentiment Gauge Function
echo "Deploying Real-time Sentiment Gauge Function..."
gcloud functions deploy real-time-sentiment-gauge \
  --gen2 \
  --runtime=$RUNTIME \
  --region=$REGION \
  --source=. \
  --entry-point=real_time_sentiment_gauge \
  --trigger-http \
  --allow-unauthenticated \
  --timeout=300s \
  --memory=512MB

# Deploy Daily Analytics Engine Function
echo "Deploying Daily Analytics Engine Function..."
gcloud functions deploy daily-analytics-engine \
  --gen2 \
  --runtime=$RUNTIME \
  --region=$REGION \
  --source=. \
  --entry-point=daily_analytics_engine \
  --trigger-http \
  --allow-unauthenticated \
  --timeout=540s \
  --memory=1GB

# Create Cloud Scheduler jobs

# Real-time Sentiment Gauge - every 15 minutes (offset by 5 minutes from Phase 1)
echo "Creating Cloud Scheduler job for real-time sentiment gauge..."
gcloud scheduler jobs create http real-time-sentiment-scheduler \
  --location=$REGION \
  --schedule="5,20,35,50 * * * *" \
  --uri="https://${REGION}-${PROJECT_ID}.cloudfunctions.net/real-time-sentiment-gauge" \
  --http-method=POST \
  --time-zone="Asia/Kolkata" \
  --description="Real-time sentiment gauge calculation every 15 minutes"

# Daily Analytics Engine - daily at 11:55 PM
echo "Creating Cloud Scheduler job for daily analytics..."
gcloud scheduler jobs create http daily-analytics-scheduler \
  --location=$REGION \
  --schedule="55 23 * * *" \
  --uri="https://${REGION}-${PROJECT_ID}.cloudfunctions.net/daily-analytics-engine" \
  --http-method=POST \
  --time-zone="Asia/Kolkata" \
  --description="Daily analytics calculation at 11:55 PM"

echo "Deployment complete!"
echo ""
echo "Function URLs:"
echo "Real-time Sentiment Gauge: https://${REGION}-${PROJECT_ID}.cloudfunctions.net/real-time-sentiment-gauge"
echo "Daily Analytics Engine: https://${REGION}-${PROJECT_ID}.cloudfunctions.net/daily-analytics-engine"
echo ""
echo "Test the functions:"
echo "curl https://${REGION}-${PROJECT_ID}.cloudfunctions.net/real-time-sentiment-gauge"
echo "curl https://${REGION}-${PROJECT_ID}.cloudfunctions.net/daily-analytics-engine"
