# 🚀 Deployment Guide

This guide walks you through deploying the Fintech AI News Platform to production.

## Prerequisites

1. **Google Cloud Account** with billing enabled
2. **Firebase Project** created
3. **Node.js 18+** and **Python 3.12+** installed locally
4. **gcloud CLI** installed and configured
5. **Firebase CLI** installed
6. **API Keys**:
   - Gemini API key from Google AI Studio
   - Financial data API key (Alpha Vantage or similar)

## Step 1: Set Up Google Cloud Project

```bash
# Install gcloud CLI if not installed
# Visit: https://cloud.google.com/sdk/docs/install

# Login to your Google Cloud account
gcloud auth login

# Create a new project (or use existing)
export PROJECT_ID="your-project-id"
gcloud projects create $PROJECT_ID --name="Fintech AI News"
gcloud config set project $PROJECT_ID

# Enable billing
gcloud beta billing projects link $PROJECT_ID --billing-account=YOUR_BILLING_ACCOUNT_ID

# Enable required APIs
gcloud services enable \
  cloudfunctions.googleapis.com \
  cloudscheduler.googleapis.com \
  secretmanager.googleapis.com \
  firestore.googleapis.com \
  redis.googleapis.com \
  vpcaccess.googleapis.com \
  run.googleapis.com
```

## Step 2: Set Up Firestore Database

```bash
# Initialize Firestore in your project
firebase init firestore --project $PROJECT_ID

# Select "Create a new Firestore database"
# Choose production mode
# Select a location (e.g., asia-south1 for Mumbai)

# Deploy Firestore rules
firebase deploy --only firestore:rules --project $PROJECT_ID
```

## Step 3: Create and Store Secrets

```bash
# Create secrets in Google Secret Manager
echo -n "YOUR_GEMINI_API_KEY" | gcloud secrets create gemini-api-key --data-file=- --replication-policy="automatic"

echo -n "YOUR_MARKET_DATA_API_KEY" | gcloud secrets create financial-api-key --data-file=- --replication-policy="automatic"

# Grant Cloud Functions access to secrets
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")

gcloud secrets add-iam-policy-binding gemini-api-key \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding financial-api-key \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

## Step 4: Create Memorystore (Redis) Instance

```bash
# Create a VPC network if not exists
gcloud compute networks create default --subnet-mode=auto || true

# Create VPC connector for accessing Memorystore
gcloud compute networks vpc-access connectors create redis-connector \
  --region=asia-south1 \
  --subnet=default \
  --min-instances=2 \
  --max-instances=10

# Create Redis instance (Basic tier for cost efficiency)
gcloud redis instances create market-data-cache \
  --size=1 \
  --region=asia-south1 \
  --tier=basic \
  --redis-version=redis_7_0

# Get Redis connection details
export REDIS_HOST=$(gcloud redis instances describe market-data-cache --region=asia-south1 --format="value(host)")
export REDIS_PORT=$(gcloud redis instances describe market-data-cache --region=asia-south1 --format="value(port)")
```

## Step 5: Deploy Cloud Functions

### Automatic Deployment (Recommended)

```bash
# Set environment variables
export PROJECT_ID="your-project-id"
export REGION="asia-south1"
export GEMINI_KEY="YOUR_GEMINI_API_KEY"
export MARKET_KEY="YOUR_MARKET_DATA_API_KEY"
export REDIS_HOST="YOUR_REDIS_HOST"
export REDIS_PORT="6379"

# Run deployment script
chmod +x deploy_all.sh
./deploy_all.sh
```

### Manual Deployment

#### Phase 1: News Pipeline

```bash
cd serverless/pipeline

# Deploy the function
gcloud functions deploy news-pipeline \
  --gen2 \
  --runtime=python312 \
  --region=asia-south1 \
  --source=. \
  --entry-point=main \
  --trigger-http \
  --allow-unauthenticated \
  --timeout=540s \
  --memory=1GB \
  --max-instances=1 \
  --concurrency=1 \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID"

# Create scheduler job
gcloud scheduler jobs create http news-pipeline-schedule \
  --location=asia-south1 \
  --schedule="*/15 * * * *" \
  --http-method=POST \
  --time-zone="Asia/Kolkata" \
  --uri="https://asia-south1-${PROJECT_ID}.cloudfunctions.net/news-pipeline"
```

#### Phase 2: Market Data API

```bash
cd serverless/marketdata

gcloud functions deploy market-data-api \
  --gen2 \
  --runtime=python312 \
  --region=asia-south1 \
  --source=. \
  --entry-point=main \
  --trigger-http \
  --allow-unauthenticated \
  --timeout=30s \
  --memory=512MB \
  --max-instances=100 \
  --vpc-connector=redis-connector \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID,REDIS_HOST=$REDIS_HOST,REDIS_PORT=$REDIS_PORT"
```

#### Phase 4: Daily Analytics

```bash
cd serverless/analytics

gcloud functions deploy daily-analytics \
  --gen2 \
  --runtime=python312 \
  --region=asia-south1 \
  --source=. \
  --entry-point=main \
  --trigger-http \
  --allow-unauthenticated \
  --timeout=900s \
  --memory=1GB \
  --max-instances=1 \
  --concurrency=1 \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID"

# Create scheduler job
gcloud scheduler jobs create http daily-analytics-schedule \
  --location=asia-south1 \
  --schedule="55 23 * * *" \
  --http-method=POST \
  --time-zone="Asia/Kolkata" \
  --uri="https://asia-south1-${PROJECT_ID}.cloudfunctions.net/daily-analytics"
```

#### AI Research API

```bash
cd serverless

gcloud functions deploy ai-research-function \
  --gen2 \
  --runtime=python312 \
  --region=asia-south1 \
  --source=ai_research_api.py \
  --entry-point=ai_research_function \
  --trigger-http \
  --allow-unauthenticated \
  --timeout=60s \
  --memory=512MB \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID"
```

## Step 6: Deploy Frontend

### Option A: Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Follow prompts to link your project
# Add environment variable:
# VITE_AI_API_URL=https://asia-south1-YOUR_PROJECT.cloudfunctions.net
```

### Option B: Netlify

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Build the project
npm run build

# Deploy
netlify deploy --prod

# Add environment variable in Netlify dashboard
# VITE_AI_API_URL=https://asia-south1-YOUR_PROJECT.cloudfunctions.net
```

### Option C: Firebase Hosting

```bash
# Initialize Firebase Hosting
firebase init hosting --project $PROJECT_ID

# Select "build" as public directory
# Configure as single-page app

# Build and deploy
npm run build
firebase deploy --only hosting --project $PROJECT_ID
```

## Step 7: Set Up Firestore Collections

The Cloud Functions will automatically create collections as they run. However, you can manually initialize:

1. Go to Firebase Console → Firestore Database
2. Create collections if needed:
   - `articles` (auto-created by pipeline)
   - `market_status` (auto-created by pipeline)
   - `sentiment_history` (auto-created by analytics)
   - `feedback` (created by users)

## Step 8: Monitor and Verify

```bash
# Check Cloud Function logs
gcloud functions logs read news-pipeline --limit=50 --region=asia-south1
gcloud functions logs read market-data-api --limit=50 --region=asia-south1

# Check Firestore data
firebase firestore:indexes

# Test API endpoints
curl https://asia-south1-${PROJECT_ID}.cloudfunctions.net/market-data-api

# Check scheduled jobs
gcloud scheduler jobs list --location=asia-south1
```

## Cost Estimation

### Monthly Costs (Approximate)

- **Cloud Functions**: $5-20 (based on invocations)
- **Firestore**: $10-30 (based on reads/writes)
- **Memorystore (Redis)**: $30 (basic tier)
- **Cloud Scheduler**: Free (within limits)
- **Storage**: $1-5
- **Network**: $2-10

**Total**: ~$50-100/month for moderate traffic

## Troubleshooting

### Functions not deploying
```bash
# Check quotas
gcloud compute project-info describe --project $PROJECT_ID

# Check service account permissions
gcloud projects get-iam-policy $PROJECT_ID
```

### Redis connection issues
```bash
# Verify VPC connector
gcloud compute networks vpc-access connectors describe redis-connector --region=asia-south1

# Test connectivity
gcloud compute instances create test-vm --zone=asia-south1-a
gcloud compute ssh test-vm --zone=asia-south1-a --command="telnet $REDIS_HOST $REDIS_PORT"
```

### Memory issues in analytics
```bash
# Increase memory allocation
gcloud functions deploy daily-analytics \
  --gen2 \
  --memory=2GB \
  # ... other flags
```

## Security Checklist

- [ ] Firestore rules deployed and tested
- [ ] Secrets stored in Secret Manager
- [ ] API keys rotated regularly
- [ ] CORS configured correctly
- [ ] Firebase App Check enabled
- [ ] HTTPS enforced on frontend
- [ ] Rate limiting configured
- [ ] Monitoring alerts set up

## Support

For issues or questions:
1. Check Cloud Logging for errors
2. Review Firestore security rules
3. Verify API quotas and limits
4. Open an issue on GitHub

## Next Steps

- Set up monitoring and alerting
- Configure custom domain
- Enable Firebase App Check
- Set up CI/CD pipeline
- Configure backup and disaster recovery

