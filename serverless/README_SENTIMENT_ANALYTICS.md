# Sentiment Analytics Engine

## Overview
Two scheduled Google Cloud Functions that aggregate raw article data into powerful analytics for the frontend application.

## Functions

### 1. Real-time Sentiment Gauge Engine
**Purpose**: Calculate current rolling market sentiment for the live gauge on the Home Page.

**Trigger**: Every 15 minutes (offset by 5 minutes from Phase 1)
- Schedule: `5,20,35,50 * * * *` (5 minutes past each quarter hour)

**Logic**:
1. Query articles from last 6 hours
2. Convert sentiment to scores: Positive=1, Neutral=0, Negative=-1
3. Calculate average sentiment score
4. Overwrite `market_status/current_sentiment` document

**Output Document** (`market_status/current_sentiment`):
```json
{
  "averageScore": 0.35,
  "lastUpdated": "2025-10-26T10:30:00Z",
  "articlesAnalyzed": 45,
  "timeWindow": "6 hours"
}
```

### 2. Daily Analytics Engine
**Purpose**: Generate historical data for trend charts on the AI Sentiment Hub.

**Trigger**: Daily at 11:55 PM
- Schedule: `55 23 * * *`

**Logic**:
1. Query all articles for the current day
2. Calculate overall daily sentiment
3. Map tickers to sectors using hardcoded dictionary
4. Calculate sector-specific sentiment scores
5. Create new document in `sentiment_history` collection

**Output Document** (`sentiment_history/2025-10-26`):
```json
{
  "date": "2025-10-26",
  "overallSentimentScore": -0.12,
  "articlesAnalyzed": 280,
  "sectorBreakdown": {
    "IT": 0.60,
    "Banking": -0.20,
    "Pharma": 0.15,
    "Auto": 0.40,
    "FMCG": -0.30,
    "Energy": -0.10,
    "Metals": 0.05,
    "Real Estate": 0.25,
    "Telecom": -0.15,
    "Power": 0.10
  },
  "lastUpdated": "2025-10-26T23:55:00Z"
}
```

## Ticker-to-Sector Mapping

The system includes a comprehensive mapping of Indian stock tickers to sectors:

### IT Sector
- TCS, INFY, WIPRO, HCLTECH, TECHM, MINDTREE, LTI, MPHASIS

### Banking Sector
- HDFCBANK, ICICIBANK, KOTAKBANK, SBIN, AXISBANK, INDUSINDBK, BANDHANBNK, FEDERALBNK

### Pharma Sector
- SUNPHARMA, DRREDDY, CIPLA, BIOCON, DIVISLAB, LUPIN, AUROPHARMA, CADILAHC

### Auto Sector
- MARUTI, TATAMOTORS, M&M, BAJAJ-AUTO, HEROMOTOCO, EICHERMOT, ASHOKLEY, TVSMOTORS

### FMCG Sector
- HINDUNILVR, ITC, NESTLEIND, DABUR, BRITANNIA, GODREJCP, MARICO, COLPAL

### Energy Sector
- RELIANCE, ONGC, GAIL, BPCL, HPCL, IOC, PETRONET, ADANIGREEN

### Additional Sectors
- Metals, Real Estate, Telecom, Power

## Database Collections

### market_status Collection
- **Document**: `current_sentiment`
- **Purpose**: Real-time sentiment gauge data
- **Update Frequency**: Every 15 minutes
- **Access**: Public read-only

### sentiment_history Collection
- **Document ID**: Date string (e.g., "2025-10-26")
- **Purpose**: Historical sentiment data for charts
- **Update Frequency**: Daily
- **Access**: Public read-only

## Security Rules

Updated Firestore rules include read-only access for new collections:

```javascript
// Market status (managed by Phase 4 serverless function)
match /market_status/{statusId} {
  allow read: if true;  // Public read access
  allow write: if false;  // No client writes - managed by serverless function
}

// Sentiment history (managed by Phase 4 serverless function)
match /sentiment_history/{historyId} {
  allow read: if true;  // Public read access
  allow write: if false;  // No client writes - managed by serverless function
}
```

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements_sentiment.txt
```

### 2. Deploy Functions
```bash
./deploy_sentiment_analytics.sh
```

### 3. Deploy Security Rules
```bash
firebase deploy --only firestore:rules
```

### 4. Verify Deployment
```bash
# Test real-time sentiment gauge
curl https://asia-south1-your-project.cloudfunctions.net/real-time-sentiment-gauge

# Test daily analytics engine
curl https://asia-south1-your-project.cloudfunctions.net/daily-analytics-engine
```

## Frontend Integration

### Real-time Sentiment Gauge
```javascript
// Listen to real-time sentiment updates
const sentimentRef = db.collection('market_status').doc('current_sentiment');
const unsubscribe = sentimentRef.onSnapshot((doc) => {
  if (doc.exists) {
    const data = doc.data();
    updateGauge(data.averageScore);
  }
});
```

### Historical Charts
```javascript
// Query historical sentiment data
const historyRef = db.collection('sentiment_history');
const query = historyRef
  .where('date', '>=', startDate)
  .where('date', '<=', endDate)
  .orderBy('date');

query.get().then((snapshot) => {
  const chartData = [];
  snapshot.forEach((doc) => {
    chartData.push(doc.data());
  });
  updateChart(chartData);
});
```

## Monitoring

### Cloud Logging
Monitor function execution:
```bash
# Real-time sentiment gauge logs
gcloud functions logs read real-time-sentiment-gauge --gen2 --region=asia-south1

# Daily analytics engine logs
gcloud functions logs read daily-analytics-engine --gen2 --region=asia-south1
```

### Key Metrics
- Function execution time
- Articles processed per run
- Sentiment score trends
- Error rates

## Performance Optimization

### Query Optimization
- Indexed queries on `publishedAt` field
- Efficient time-based filtering
- Batch processing for large datasets

### Caching Strategy
- Real-time gauge: Single document overwrite
- Historical data: Date-based document IDs
- Efficient frontend queries

### Error Handling
- Graceful degradation on empty datasets
- Comprehensive logging
- Fallback to neutral sentiment (0.0)

## Cost Estimation

### Cloud Functions
- **Real-time gauge**: ~$2-5/month (96 executions/day)
- **Daily analytics**: ~$0.50/month (30 executions/month)

### Firestore
- **Reads**: Minimal (single document reads)
- **Writes**: ~$1-2/month (overwrites + new documents)

### Total Estimated Cost
- **Monthly**: $3-7 (depending on article volume)

## Troubleshooting

### Common Issues

1. **"No articles found"**
   - Check Phase 1 function is running
   - Verify article collection has data
   - Check time window calculations

2. **"Permission denied"**
   - Verify Firestore security rules
   - Check function service account permissions
   - Ensure Firebase initialization

3. **"Sector mapping errors"**
   - Check ticker-to-sector dictionary
   - Verify ticker format (uppercase)
   - Review article ticker extraction

4. **"Function timeout"**
   - Increase function timeout
   - Optimize query performance
   - Check article volume

### Debug Mode
Enable detailed logging:
```python
logging.basicConfig(level=logging.DEBUG)
```

## Local Testing

### Test Functions
```bash
python sentiment_analytics.py
```

### Test with Sample Data
```python
# Create test articles
test_articles = [
    {"sentiment": "Positive", "tickers": ["TCS", "INFY"]},
    {"sentiment": "Negative", "tickers": ["HDFCBANK"]},
    {"sentiment": "Neutral", "tickers": ["RELIANCE"]}
]

# Test calculations
analytics = SentimentAnalytics()
sentiment_data = analytics.calculate_real_time_sentiment()
analytics_data = analytics.calculate_daily_analytics()
```

## Future Enhancements

### Advanced Analytics
- Sentiment trend analysis
- Sector correlation analysis
- Market volatility indicators
- Predictive sentiment modeling

### Performance Improvements
- Parallel processing for large datasets
- Incremental updates
- Advanced caching strategies
- Real-time streaming analytics

### Additional Features
- Custom time windows
- Sector-specific alerts
- Sentiment confidence scores
- Multi-language support

## Support
For issues or questions:
1. Check Cloud Logging for errors
2. Verify function deployment status
3. Test with sample data
4. Contact development team
