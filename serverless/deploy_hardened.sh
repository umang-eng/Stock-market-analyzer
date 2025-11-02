#!/bin/bash
# Deployment script for Hardened News Pipeline Cloud Function

PROJECT_ID="your-project-id"  # Replace with your GCP project ID
FUNCTION_NAME="news-pipeline-hardened"
REGION="asia-south1"  # Mumbai region for Indian context
RUNTIME="python312"

# Set GCP project
gcloud config set project $PROJECT_ID

# Create secret for Gemini API key (if not exists)
echo "Creating secret for Gemini API key..."
echo "your-gemini-api-key-here" | gcloud secrets create gemini-api-key --data-file=- || echo "Secret already exists"

# Deploy the hardened function with SRE fixes
echo "Deploying hardened news pipeline function..."
gcloud functions deploy $FUNCTION_NAME \
  --gen2 \
  --runtime=$RUNTIME \
  --region=$REGION \
  --source=. \
  --entry-point=news_pipeline_hardened \
  --trigger-http \
  --allow-unauthenticated \
  --timeout=540s \
  --memory=1GB \
  --max-instances=1 \
  --concurrency=1 \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID"

# Create Cloud Scheduler job (offset by 5 minutes from original)
echo "Creating Cloud Scheduler job..."
gcloud scheduler jobs create http ${FUNCTION_NAME}-scheduler \
  --location=$REGION \
  --schedule="5,20,35,50 * * * *" \
  --uri="https://${REGION}-${PROJECT_ID}.cloudfunctions.net/${FUNCTION_NAME}" \
  --http-method=POST \
  --time-zone="Asia/Kolkata" \
  --description="Hardened news pipeline with SRE fixes - every 15 minutes"

echo "Deployment complete!"
echo ""
echo "SRE Fixes Applied:"
echo "✅ Single Gemini API call (cost reduction ~95%)"
echo "✅ Batch duplicate checking (N+1 query fix)"
echo "✅ Pydantic validation (data integrity)"
echo "✅ Secret Manager integration (security)"
echo "✅ Concurrency=1 (race condition prevention)"
echo "✅ Increased timeout (540s)"
echo "✅ Max instances=1 (resource control)"
echo ""
echo "Function URL: https://${REGION}-${PROJECT_ID}.cloudfunctions.net/${FUNCTION_NAME}"
echo ""
echo "Test the function:"
echo "curl https://${REGION}-${PROJECT_ID}.cloudfunctions.net/${FUNCTION_NAME}"
