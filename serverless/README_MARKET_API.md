# Market Data API - Secure Financial Data Proxy

## Overview
Secure Google Cloud Function that acts as a proxy to third-party financial data APIs, providing cached market data for the frontend application.

## Features
- 🔒 **Secure**: API keys stored in Secret Manager
- ⚡ **Fast**: 5-minute caching layer
- 🛡️ **Reliable**: Fallback to stale cache on API failures
- 🌐 **CORS-enabled**: Secure cross-origin requests
- 📊 **Comprehensive**: Indices, gainers, losers, sectors

## API Endpoints

### GET /market-data
Returns current market data in the following format:

```json
{
  "indices": [
    {
      "name": "NIFTY 50",
      "price": 24150.75,
      "change": 120.25,
      "changePercent": 0.50
    },
    {
      "name": "SENSEX", 
      "price": 78450.10,
      "change": 400.50,
      "changePercent": 0.51
    }
  ],
  "gainers": [
    {
      "ticker": "LT",
      "name": "Larsen & Toubro",
      "price": 3500.00,
      "changePercent": 5.2
    }
  ],
  "losers": [
    {
      "ticker": "HDFCBANK",
      "name": "HDFC Bank", 
      "price": 1600.00,
      "changePercent": -2.1
    }
  ],
  "sectors": [
    {
      "name": "IT",
      "changePercent": 1.2
    },
    {
      "name": "Banking",
      "changePercent": -0.5
    }
  ]
}
```

### GET /health
Health check endpoint returning service status.

## Setup Instructions

### 1. Prerequisites
- Google Cloud Project with billing enabled
- Firebase project set up
- Third-party financial API key (Alpha Vantage, Finnhub, etc.)

### 2. Install Dependencies
```bash
pip install -r requirements_market_api.txt
```

### 3. Configure API Key
Store your financial API key in Secret Manager:

```bash
# Create secret
echo "your-api-key-here" | gcloud secrets create financial-api-key --data-file=-

# Or update existing secret
echo "your-api-key-here" | gcloud secrets versions add financial-api-key --data-file=-
```

### 4. Deploy Function
```bash
./deploy_market_api.sh
```

### 5. Test Endpoint
```bash
curl https://asia-south1-your-project.cloudfunctions.net/market-data-api/market-data
```

## Caching Strategy

### Cache Duration
- **Fresh data**: 5 minutes
- **Stale fallback**: Up to 24 hours (if API fails)

### Cache Storage
- **Location**: Firestore collection `market_data_cache`
- **Document**: `latest_data`
- **Fields**: `market_data`, `cached_at`, `created_at`

### Cache Logic
1. Check Firestore for cached data
2. If cache < 5 minutes old → return cached data
3. If cache > 5 minutes old → fetch fresh data
4. If API fails → return stale cache (if available)
5. If no cache → return empty structure

## Security Features

### CORS Configuration
```python
CORS(app, origins=[
    "http://localhost:5173",  # Local development
    "https://your-domain.com", # Production domain
])
```

### API Key Security
- Stored in Google Secret Manager
- Retrieved at runtime
- Never logged or exposed

### Optional App Check
Uncomment Firebase App Check validation:
```python
app_check_token = request.headers.get('X-Firebase-AppCheck')
if not verify_app_check_token(app_check_token):
    return jsonify({"error": "Invalid App Check token"}), 401
```

## Error Handling

### API Failures
- Logs errors to Cloud Logging
- Returns stale cache if available
- Graceful degradation to empty data

### Retry Logic
- 10-second timeout per API call
- Exponential backoff for retries
- Circuit breaker pattern

## Performance Optimization

### Caching Benefits
- **Cost reduction**: Fewer API calls
- **Speed**: Sub-second response times
- **Reliability**: Works even if APIs are down

### Memory Usage
- **Allocated**: 512MB
- **Typical usage**: ~100MB
- **Peak usage**: ~200MB

## Monitoring

### Cloud Logging
View logs in Google Cloud Console:
```bash
gcloud functions logs read market-data-api --gen2 --region=asia-south1
```

### Key Metrics
- Cache hit rate
- API response times
- Error rates
- Function execution time

## Cost Estimation

### Cloud Function
- **Invocations**: ~$0.40 per million
- **Compute time**: ~$0.0000025 per GB-second
- **Estimated monthly**: $5-15 (depending on usage)

### Firestore
- **Reads**: 50K free per day
- **Writes**: 20K free per day
- **Estimated monthly**: $0-5

### Third-party APIs
- **Alpha Vantage**: 5 calls/minute free, $49.99/month for premium
- **Finnhub**: 60 calls/minute free, $9/month for basic

## Troubleshooting

### Common Issues

1. **"No API key available"**
   - Check Secret Manager configuration
   - Verify secret name matches code

2. **"CORS error"**
   - Add your domain to CORS origins
   - Check preflight requests

3. **"Cache not working"**
   - Verify Firestore permissions
   - Check collection/document names

4. **"API timeout"**
   - Increase function timeout
   - Check third-party API status

### Debug Mode
Enable debug logging:
```python
logging.basicConfig(level=logging.DEBUG)
```

## Local Development

### Run Locally
```bash
python market_data_api.py
```

### Test Endpoints
```bash
# Market data
curl http://localhost:8080/market-data

# Health check
curl http://localhost:8080/health
```

## Production Considerations

### Scaling
- Cloud Functions auto-scale
- Consider regional deployment
- Monitor cold start times

### Security
- Enable App Check in production
- Use VPC connector if needed
- Implement rate limiting

### Monitoring
- Set up alerts for errors
- Monitor API quota usage
- Track cache performance

## Support
For issues, check Cloud Logging or contact the development team.
