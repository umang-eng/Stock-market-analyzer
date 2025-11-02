#!/bin/bash
# Deployment script for Market Data API Cloud Function

PROJECT_ID="your-project-id"  # Replace with your GCP project ID
FUNCTION_NAME="market-data-api"
REGION="asia-south1"  # Mumbai region for Indian context
RUNTIME="python312"

# Set GCP project
gcloud config set project $PROJECT_ID

# Create secret for API key (if not exists)
echo "Creating secret for financial API key..."
gcloud secrets create financial-api-key --data-file=- <<< "your-api-key-here" || echo "Secret already exists"

# Deploy the function
gcloud functions deploy $FUNCTION_NAME \
  --gen2 \
  --runtime=$RUNTIME \
  --region=$REGION \
  --source=. \
  --entry-point=market_data_function \
  --trigger-http \
  --allow-unauthenticated \
  --timeout=300s \
  --memory=512MB \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID"

echo "Deployment complete!"
echo "Function URL: https://${REGION}-${PROJECT_ID}.cloudfunctions.net/${FUNCTION_NAME}"
echo ""
echo "Test the endpoint:"
echo "curl https://${REGION}-${PROJECT_ID}.cloudfunctions.net/${FUNCTION_NAME}/market-data"
