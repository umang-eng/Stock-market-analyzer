#!/bin/bash
# Deployment script for Google Cloud Function

PROJECT_ID="your-project-id"  # Replace with your GCP project ID
FUNCTION_NAME="news-pipeline"
REGION="asia-south1"  # Mumbai region for Indian context
RUNTIME="python312"

# Set GCP project
gcloud config set project $PROJECT_ID

# Deploy the function
gcloud functions deploy $FUNCTION_NAME \
  --gen2 \
  --runtime=$RUNTIME \
  --region=$REGION \
  --source=. \
  --entry-point=news_pipeline \
  --trigger-http \
  --allow-unauthenticated \
  --timeout=540s \
  --memory=1GB \
  --set-env-vars="GEMINI_API_KEY=your-gemini-api-key"

# Create Cloud Scheduler job to trigger every 15 minutes
gcloud scheduler jobs create http ${FUNCTION_NAME}-scheduler \
  --location=$REGION \
  --schedule="*/15 * * * *" \
  --uri="https://${REGION}-${PROJECT_ID}.cloudfunctions.net/${FUNCTION_NAME}" \
  --http-method=POST \
  --time-zone="Asia/Kolkata"

echo "Deployment complete!"
echo "Function URL: https://${REGION}-${PROJECT_ID}.cloudfunctions.net/${FUNCTION_NAME}"
