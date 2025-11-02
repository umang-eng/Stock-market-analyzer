#!/bin/bash
# Deployment script for Hardened Market Data API Cloud Function

PROJECT_ID="your-project-id"  # Replace with your GCP project ID
FUNCTION_NAME="market-data-api-hardened"
REGION="asia-south1"  # Mumbai region for Indian context
RUNTIME="python312"
VPC_CONNECTOR_NAME="redis-connector"  # VPC connector for Memorystore access

# Set GCP project
gcloud config set project $PROJECT_ID

# Create Memorystore Redis instance (if not exists)
echo "Creating Memorystore Redis instance..."
gcloud redis instances create market-data-cache \
  --size=1 \
  --region=$REGION \
  --redis-version=redis_7_0 \
  --tier=basic \
  --network=projects/$PROJECT_ID/global/networks/default \
  --reserved-ip-range=10.0.0.0/29 \
  --display-name="Market Data Cache" || echo "Redis instance may already exist"

# Get Redis instance details
REDIS_HOST=$(gcloud redis instances describe market-data-cache --region=$REGION --format="value(host)")
REDIS_PORT=$(gcloud redis instances describe market-data-cache --region=$REGION --format="value(port)")

echo "Redis instance details:"
echo "Host: $REDIS_HOST"
echo "Port: $REDIS_PORT"

# Create VPC connector (if not exists)
echo "Creating VPC connector..."
gcloud compute networks vpc-access connectors create $VPC_CONNECTOR_NAME \
  --region=$REGION \
  --subnet=default \
  --subnet-project=$PROJECT_ID \
  --min-instances=2 \
  --max-instances=10 || echo "VPC connector may already exist"

# Create secret for API key (if not exists)
echo "Creating secret for financial API key..."
echo "your-api-key-here" | gcloud secrets create financial-api-key --data-file=- || echo "Secret already exists"

# Deploy the hardened function with all SRE fixes
echo "Deploying hardened market data API function..."
gcloud functions deploy $FUNCTION_NAME \
  --gen2 \
  --runtime=$RUNTIME \
  --region=$REGION \
  --source=. \
  --entry-point=market_data_function_hardened \
  --trigger-http \
  --allow-unauthenticated \
  --timeout=30s \
  --memory=512MB \
  --max-instances=100 \
  --vpc-connector=$VPC_CONNECTOR_NAME \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID,REDIS_HOST=$REDIS_HOST,REDIS_PORT=$REDIS_PORT"

echo "Deployment complete!"
echo ""
echo "SRE Fixes Applied:"
echo "✅ Redis caching (high-performance in-memory cache)"
echo "✅ Firebase App Check authentication"
echo "✅ Stale-while-revalidate resilience"
echo "✅ Comprehensive timeout handling (30s function, 10s API calls)"
echo "✅ VPC connector for Memorystore access"
echo "✅ Error handling with graceful degradation"
echo "✅ Service unavailable responses (503) for complete failures"
echo ""
echo "Function URL: https://${REGION}-${PROJECT_ID}.cloudfunctions.net/${FUNCTION_NAME}"
echo ""
echo "Test the function:"
echo "curl -H 'X-Firebase-AppCheck: your-token' https://${REGION}-${PROJECT_ID}.cloudfunctions.net/${FUNCTION_NAME}/market-data"
echo ""
echo "Health check:"
echo "curl https://${REGION}-${PROJECT_ID}.cloudfunctions.net/${FUNCTION_NAME}/health"
