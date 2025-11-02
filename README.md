# 📊 Fintech AI News Platform

A production-ready, AI-powered stock market news analysis platform that aggregates and analyzes Indian financial news in real-time using Google's Gemini AI.

## 🚀 Features

- **AI-Powered News Analysis**: Automatically fetches, analyzes, and categorizes stock market news from top Indian financial sources
- **Real-time Market Data**: Live indices, gainers/losers, and sector performance with intelligent caching
- **Sentiment Analysis**: AI-generated sentiment scores for overall market and individual sectors
- **Personalized Watchlist**: Track your favorite stocks with personalized news feeds
- **Professional AI Research**: Get comprehensive stock market insights powered by Gemini AI with Google Search grounding
- **Beautiful Dark UI**: Modern, responsive design built with React and Tailwind CSS

## 🏗️ Architecture

### Frontend
- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS
- **State Management**: React Hooks
- **Deployment**: Ready for Vercel/Netlify

### Backend (Google Cloud)
- **Phase 1**: News Pipeline (Cloud Function) - Fetches and analyzes news every 15 minutes
- **Phase 2**: Market Data API (Cloud Function) - Serves live market data with Redis caching
- **Phase 3**: User Personalization (Firebase Auth + Firestore) - Watchlists and feedback
- **Phase 4**: Daily Analytics (Cloud Function) - Historical sentiment trends

### Key Technologies
- **AI/ML**: Google Gemini API with Google Search grounding
- **Database**: Firebase Firestore
- **Cache**: Google Cloud Memorystore (Redis)
- **Secrets**: Google Secret Manager
- **Security**: Firebase App Check, CORS, Firestore Security Rules

## 📁 Project Structure

```
Stock analiser/
├── src/                          # Frontend React app
│   ├── components/               # React components
│   │   ├── Navbar.jsx           # Navigation bar
│   │   ├── MarketOverview.jsx   # Market data visualization
│   │   ├── NewsFeed.jsx         # News articles feed
│   │   ├── SentimentHub.jsx     # Sentiment analytics
│   │   ├── Watchlist.jsx        # User watchlist
│   │   ├── AIResearch.jsx       # AI research page
│   │   ├── HowItWorks.jsx       # About page
│   │   └── Contact.jsx          # Contact form
│   ├── services/                 # API services
│   │   └── api.js               # Backend API client
│   ├── App.jsx                   # Main app component
│   ├── main.jsx                  # Entry point
│   └── index.css                 # Global styles
├── mock-backend/                 # Local development server
│   └── server.js                # Express mock API
├── serverless/                   # Cloud Functions
│   ├── pipeline/                # Phase 1: News pipeline
│   │   ├── main.py              # News fetching & analysis
│   │   └── requirements.txt
│   ├── marketdata/              # Phase 2: Market data API
│   │   ├── main.py              # Live market data
│   │   └── requirements.txt
│   ├── analytics/               # Phase 4: Daily analytics
│   │   ├── main.py              # Historical sentiment
│   │   └── requirements.txt
│   ├── ai_research_api.py       # AI research endpoint
│   └── firestore.rules          # Database security rules
├── deploy_all.sh                # Deployment script
└── README.md                    # This file
```

## 🛠️ Setup & Installation

### Prerequisites
- Node.js 18+ and npm
- Python 3.12+
- Google Cloud account with billing enabled
- Firebase project

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd "Stock analiser"
   ```

2. **Install frontend dependencies**
   ```bash
   npm install
   ```

3. **Install mock backend dependencies**
   ```bash
   cd mock-backend
   npm install
   ```

4. **Start the mock backend**
   ```bash
   cd mock-backend
   node server.js
   ```
   The mock backend will run on `http://localhost:3001`

5. **Start the frontend** (in a new terminal)
   ```bash
   npm run dev
   ```
   The app will run on `http://localhost:5173`

### Cloud Deployment

1. **Set up Google Cloud**
   ```bash
   export PROJECT_ID="your-project-id"
   export REGION="asia-south1"
   export GEMINI_KEY="your-gemini-api-key"
   export MARKET_KEY="your-market-data-api-key"
   
   gcloud config set project $PROJECT_ID
   ```

2. **Run deployment script**
   ```bash
   chmod +x deploy_all.sh
   ./deploy_all.sh
   ```

3. **Deploy Firestore rules**
   ```bash
   firebase deploy --only firestore:rules --project="$PROJECT_ID"
   ```

4. **Update frontend environment**
   ```bash
   echo "VITE_AI_API_URL=https://$REGION-$PROJECT_ID.cloudfunctions.net" > .env
   ```

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```env
# Development
VITE_AI_API_URL=http://localhost:3001

# Production
# VITE_AI_API_URL=https://asia-south1-your-project.cloudfunctions.net
```

## 📖 API Endpoints

### Mock Backend (Development)
- `GET /market-data` - Market indices, gainers, losers
- `GET /articles` - List of analyzed news articles
- `GET /current-sentiment` - Current market sentiment
- `GET /sentiment-history` - Historical sentiment trends
- `POST /ai/research` - AI research query
- `POST /feedback` - Submit feedback

### Production APIs
- `https://asia-south1-PROJECT.cloudfunctions.net/market-data-api` - Market data
- `https://asia-south1-PROJECT.cloudfunctions.net/news-pipeline` - News pipeline
- `https://asia-south1-PROJECT.cloudfunctions.net/daily-analytics` - Analytics
- `https://asia-south1-PROJECT.cloudfunctions.net/ai-research-function` - AI research

## 🎨 Pages

1. **Market Overview** - Live market data, indices, and sector performance
2. **All News** - Browse all AI-analyzed news with filters
3. **Sentiment Hub** - Market sentiment trends and sector analysis
4. **My Watchlist** - Personalized stock tracking
5. **AI Research** - Professional AI-powered research tool
6. **How It Works** - Platform explanation and technology
7. **Contact** - Feedback and contact form

## 🔒 Security Features

- **Firebase App Check** - API endpoint protection
- **Firestore Security Rules** - Database access control
- **CORS** - Cross-origin request protection
- **Secret Manager** - Secure API key storage
- **Rate Limiting** - Abuse prevention
- **Data Validation** - Pydantic models for AI responses

## 💰 Cost Optimization

- **Redis Caching** - Reduces API calls and latency
- **Single Gemini Calls** - Batched article processing
- **Concurrency Control** - Prevents duplicate function executions
- **Stale-While-Revalidate** - Ensures availability during failures
- **Batched Queries** - Prevents OOM errors in analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## ⚠️ Disclaimer

This application is for informational and educational purposes only. All AI-generated analysis does not constitute financial advice. Always consult a qualified financial advisor before making investment decisions.

## 👨‍💻 Author

**Umang** - [GitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Google Gemini AI for powerful natural language understanding
- Firebase for backend infrastructure
- React and Tailwind CSS communities
- Indian financial news sources: Moneycontrol, Economic Times, Livemint, Business Standard

