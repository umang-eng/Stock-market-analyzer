#!/usr/bin/env bash
set -euo pipefail

export PROJECT_ID="studio-315816986-dfee9"
export REGION="asia-south1"
export GEMINI_KEY="AIzaSyD1aV_gDikKk3ZOaCKbmoy1c7Z2FkSgJhU"
export MARKET_KEY="ZY71HF540UK7S0M4"

echo "== Using project: $PROJECT_ID ($REGION) =="
gcloud config set project "$PROJECT_ID"

echo "== Enable services =="
gcloud services enable \
  cloudfunctions.googleapis.com \
  cloudscheduler.googleapis.com \
  secretmanager.googleapis.com \
  firestore.googleapis.com \
  redis.googleapis.com \
  vpcaccess.googleapis.com

echo "== Create/update secrets =="
if ! gcloud secrets describe gemini-api-key >/dev/null 2>&1; then
  echo -n "$GEMINI_KEY" | gcloud secrets create gemini-api-key --data-file=-
else
  echo -n "$GEMINI_KEY" | gcloud secrets versions add gemini-api-key --data-file=-
fi
if ! gcloud secrets describe financial-api-key >/dev/null 2>&1; then
  echo -n "$MARKET_KEY" | gcloud secrets create financial-api-key --data-file=-
else
  echo -n "$MARKET_KEY" | gcloud secrets versions add financial-api-key --data-file=-
fi
unset GEMINI_KEY MARKET_KEY

echo "== Create Memorystore (if needed) =="
gcloud redis instances create market-data-cache \
  --size=1 --region="$REGION" --tier=basic --redis-version=redis_7_0 || true

export REDIS_HOST="$(gcloud redis instances describe market-data-cache --region="$REGION" --format="value(host)")"
export REDIS_PORT="$(gcloud redis instances describe market-data-cache --region="$REGION" --format="value(port)")"

echo "== Create VPC connector (if needed) =="
gcloud compute networks vpc-access connectors create redis-connector \
  --region="$REGION" --subnet=default --min-instances=2 --max-instances=10 || true

echo "== Deploy Phase 2: Market Data API =="
pushd marketdata >/dev/null
gcloud functions deploy market-data-api \
  --gen2 --runtime=python312 --region="$REGION" \
  --source=. --entry-point=main --trigger-http --allow-unauthenticated \
  --timeout=30s --memory=512MB --max-instances=100 \
  --vpc-connector=redis-connector \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID,REDIS_HOST=$REDIS_HOST,REDIS_PORT=$REDIS_PORT"
popd >/dev/null

echo "== Deploy Phase 1: Pipeline =="
pushd pipeline >/dev/null
gcloud functions deploy news-pipeline \
  --gen2 --runtime=python312 --region="$REGION" \
  --source=. --entry-point=main --trigger-http --allow-unauthenticated \
  --timeout=540s --memory=1GB --max-instances=1 --concurrency=1 \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID"
popd >/dev/null

echo "== Scheduler for Phase 1 =="
gcloud scheduler jobs create http news-pipeline-schedule \
  --location="$REGION" --schedule="5,20,35,50 * * * *" \
  --http-method=POST --time-zone="Asia/Kolkata" \
  --uri="https://$REGION-$PROJECT_ID.cloudfunctions.net/news-pipeline" || true

echo "== Deploy Phase 4: Daily Analytics =="
pushd analytics >/dev/null
gcloud functions deploy daily-analytics \
  --gen2 --runtime=python312 --region="$REGION" \
  --source=. --entry-point=main --trigger-http --allow-unauthenticated \
  --timeout=900s --memory=1GB --max-instances=1 --concurrency=1 \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID"
popd >/dev/null

echo "== Scheduler for Phase 4 =="
gcloud scheduler jobs create http daily-analytics-schedule \
  --location="$REGION" --schedule="55 23 * * *" \
  --http-method=POST --time-zone="Asia/Kolkata" \
  --uri="https://$REGION-$PROJECT_ID.cloudfunctions.net/daily-analytics" || true

echo "== Deploy Firestore rules =="
firebase deploy --only firestore:rules --project="$PROJECT_ID" --config serverless/firestore.rules

echo "== Frontend env =="
echo "VITE_AI_API_URL=https://$REGION-$PROJECT_ID.cloudfunctions.net" > .env

echo "== Done. Function URLs =="
echo "Pipeline:        https://$REGION-$PROJECT_ID.cloudfunctions.net/news-pipeline"
echo "Daily analytics: https://$REGION-$PROJECT_ID.cloudfunctions.net/daily-analytics"
echo "Market data:     https://$REGION-$PROJECT_ID.cloudfunctions.net/market-data-api/market-data"
