#!/bin/bash
# Deployment script for Hardened Phase 3 & 4 (SRE Audit Fixes)

PROJECT_ID="your-project-id"  # Replace with your GCP project ID
REGION="asia-south1"  # Mumbai region for Indian context
RUNTIME="python312"

# Set GCP project
gcloud config set project $PROJECT_ID

echo "=== SRE Audit Fixes Deployment ==="
echo ""

# Deploy Phase 1 with integrated sentiment (replaces separate 15-min function)
echo "1. Deploying Phase 1 with integrated sentiment analysis..."
gcloud functions deploy news-pipeline-hardened-with-sentiment \
  --gen2 \
  --runtime=$RUNTIME \
  --region=$REGION \
  --source=. \
  --entry-point=news_pipeline_hardened_with_sentiment \
  --trigger-http \
  --allow-unauthenticated \
  --timeout=540s \
  --memory=1GB \
  --max-instances=1 \
  --concurrency=1 \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID"

# Update Cloud Scheduler for Phase 1 (now includes sentiment)
echo "2. Updating Cloud Scheduler for integrated pipeline..."
gcloud scheduler jobs create http news-pipeline-integrated-scheduler \
  --location=$REGION \
  --schedule="5,20,35,50 * * * *" \
  --uri="https://${REGION}-${PROJECT_ID}.cloudfunctions.net/news-pipeline-hardened-with-sentiment" \
  --http-method=POST \
  --time-zone="Asia/Kolkata" \
  --description="Integrated news pipeline with sentiment analysis - every 15 minutes" || echo "Scheduler may already exist"

# Deploy Phase 4 Daily Analytics (hardened with batched queries)
echo "3. Deploying Phase 4 Daily Analytics Engine..."
gcloud functions deploy daily-analytics-engine-hardened \
  --gen2 \
  --runtime=$RUNTIME \
  --region=$REGION \
  --source=. \
  --entry-point=daily_analytics_engine_hardened \
  --trigger-http \
  --allow-unauthenticated \
  --timeout=900s \
  --memory=1GB \
  --max-instances=1 \
  --concurrency=1 \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID"

# Create Cloud Scheduler for Daily Analytics
echo "4. Creating Cloud Scheduler for daily analytics..."
gcloud scheduler jobs create http daily-analytics-scheduler \
  --location=$REGION \
  --schedule="55 23 * * *" \
  --uri="https://${REGION}-${PROJECT_ID}.cloudfunctions.net/daily-analytics-engine-hardened" \
  --http-method=POST \
  --time-zone="Asia/Kolkata" \
  --description="Daily analytics engine with batched queries - daily at 11:55 PM" || echo "Scheduler may already exist"

# Deploy hardened Firestore rules
echo "5. Deploying hardened Firestore security rules..."
firebase deploy --only firestore:rules --project=$PROJECT_ID

echo ""
echo "=== Deployment Complete ==="
echo ""
echo "SRE Fixes Applied:"
echo "✅ Phase 1: Integrated sentiment analysis (eliminated redundant function)"
echo "✅ Phase 3: Hardened Firestore rules with data validation and rate limiting"
echo "✅ Phase 4: Batched queries preventing OOM crashes"
echo "✅ Sector data from Phase 1 (eliminated ticker mapping maintenance)"
echo "✅ Rate limiting for feedback submissions"
echo "✅ Data validation for watchlist items"
echo "✅ Memory optimization for large datasets"
echo ""
echo "Function URLs:"
echo "- Phase 1 (Integrated): https://${REGION}-${PROJECT_ID}.cloudfunctions.net/news-pipeline-hardened-with-sentiment"
echo "- Phase 4 (Daily): https://${REGION}-${PROJECT_ID}.cloudfunctions.net/daily-analytics-engine-hardened"
echo ""
echo "Test functions:"
echo "curl https://${REGION}-${PROJECT_ID}.cloudfunctions.net/news-pipeline-hardened-with-sentiment"
echo "curl https://${REGION}-${PROJECT_ID}.cloudfunctions.net/daily-analytics-engine-hardened"
