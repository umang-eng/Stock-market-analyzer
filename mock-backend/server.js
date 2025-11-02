const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const PORT = 3001;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Mock data generators
const generateMockNews = () => [
  {
    id: '1',
    headline: 'Reliance Industries Reports Strong Q3 Earnings, Stock Surges 5%',
    source: 'The Economic Times',
    summary: 'Reliance Industries posted robust quarterly results with revenue growth of 12% year-over-year, driven by strong performance in digital services and retail segments.',
    sentiment: 'Positive',
    publishedAt: new Date().toISOString(),
    tickers: ['RELIANCE'],
    sectors: ['Energy', 'Retail']
  },
  {
    id: '2',
    headline: 'TCS Wins Major Digital Transformation Deal Worth $2.5B',
    source: 'Moneycontrol',
    summary: 'Tata Consultancy Services secured a significant digital transformation contract from a global financial services company, expected to boost revenue significantly.',
    sentiment: 'Positive',
    publishedAt: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
    tickers: ['TCS'],
    sectors: ['IT']
  },
  {
    id: '3',
    headline: 'Banking Sector Faces Headwinds Amid Rising Interest Rates',
    source: 'Livemint',
    summary: 'Indian banking sector experiencing pressure due to increasing interest rates and regulatory changes, with potential impact on lending growth.',
    sentiment: 'Negative',
    publishedAt: new Date(Date.now() - 60 * 60 * 1000).toISOString(),
    tickers: ['HDFCBANK', 'ICICIBANK', 'SBIN'],
    sectors: ['Banking']
  },
  {
    id: '4',
    headline: 'Pharma Companies See Mixed Results in Q3 Earnings Season',
    source: 'Business Standard',
    summary: 'Pharmaceutical sector shows mixed performance with some companies reporting strong growth while others face regulatory challenges.',
    sentiment: 'Neutral',
    publishedAt: new Date(Date.now() - 90 * 60 * 1000).toISOString(),
    tickers: ['SUNPHARMA', 'DRREDDY'],
    sectors: ['Pharma']
  },
  {
    id: '5',
    headline: 'Auto Sector Recovery Continues with Strong Domestic Sales',
    source: 'Financial Express',
    summary: 'Automobile manufacturers report continued recovery in domestic sales, with Maruti Suzuki and Mahindra leading the growth.',
    sentiment: 'Positive',
    publishedAt: new Date(Date.now() - 120 * 60 * 1000).toISOString(),
    tickers: ['MARUTI', 'M&M'],
    sectors: ['Auto']
  }
];

const generateMockMarketData = () => ({
  indices: [
    {
      name: 'NIFTY 50',
      price: 24150.75,
      change: 120.25,
      changePercent: 0.50
    },
    {
      name: 'SENSEX',
      price: 78450.10,
      change: 400.50,
      changePercent: 0.51
    }
  ],
  gainers: [
    { ticker: 'LT', name: 'Larsen & Toubro', price: 3500.00, changePercent: 5.2 },
    { ticker: 'M&M', name: 'Mahindra & Mahindra', price: 2900.00, changePercent: 4.8 },
    { ticker: 'RELIANCE', name: 'Reliance Industries', price: 2450.00, changePercent: 3.5 },
    { ticker: 'TCS', name: 'Tata Consultancy', price: 3200.00, changePercent: 2.8 },
    { ticker: 'HDFCBANK', name: 'HDFC Bank', price: 1650.00, changePercent: 2.1 }
  ],
  losers: [
    { ticker: 'INFY', name: 'Infosys', price: 1500.00, changePercent: -1.8 },
    { ticker: 'WIPRO', name: 'Wipro', price: 420.00, changePercent: -1.5 },
    { ticker: 'ONGC', name: 'Oil & Natural Gas', price: 245.00, changePercent: -1.2 },
    { ticker: 'NTPC', name: 'NTPC', price: 265.00, changePercent: -0.9 },
    { ticker: 'COALINDIA', name: 'Coal India', price: 385.00, changePercent: -0.7 }
  ],
  sectors: [
    { name: 'IT', changePercent: 1.2 },
    { name: 'Banking', changePercent: -0.5 },
    { name: 'Auto', changePercent: 1.8 },
    { name: 'Pharma', changePercent: 0.3 },
    { name: 'FMCG', changePercent: -0.2 },
    { name: 'Energy', changePercent: 0.8 },
    { name: 'Metals', changePercent: -0.4 },
    { name: 'RealEstate', changePercent: 0.6 }
  ],
  lastUpdated: new Date().toISOString()
});

const generateMockSentimentData = () => ({
  currentSentiment: {
    averageScore: 0.35,
    lastUpdated: new Date().toISOString(),
    articlesAnalyzed: 45,
    timeWindow: '6 hours'
  },
  historicalData: [
    { date: '2024-10-21', overallSentimentScore: 0.42, articlesAnalyzed: 280 },
    { date: '2024-10-22', overallSentimentScore: 0.38, articlesAnalyzed: 295 },
    { date: '2024-10-23', overallSentimentScore: 0.31, articlesAnalyzed: 310 },
    { date: '2024-10-24', overallSentimentScore: 0.28, articlesAnalyzed: 275 },
    { date: '2024-10-25', overallSentimentScore: 0.35, articlesAnalyzed: 290 },
    { date: '2024-10-26', overallSentimentScore: 0.41, articlesAnalyzed: 285 },
    { date: '2024-10-27', overallSentimentScore: 0.35, articlesAnalyzed: 45 }
  ],
  sectorBreakdown: {
    IT: 0.60,
    Banking: -0.20,
    Pharma: 0.15,
    Auto: 0.40,
    FMCG: -0.30,
    Energy: 0.10,
    Metals: 0.05,
    RealEstate: 0.25,
    Telecom: -0.15,
    Power: 0.10
  }
});

// API Routes

// Health check
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    timestamp: new Date().toISOString(),
    service: 'mock-backend'
  });
});

// Market data API (Phase 2)
app.get('/market-data', (req, res) => {
  console.log('📊 Market data requested');
  const marketData = generateMockMarketData();
  res.json(marketData);
});

// News articles API (Phase 1)
app.get('/articles', (req, res) => {
  console.log('📰 Articles requested');
  const articles = generateMockNews();
  res.json(articles);
});

// Sentiment data API (Phase 4)
app.get('/sentiment/current', (req, res) => {
  console.log('🧠 Current sentiment requested');
  const sentimentData = generateMockSentimentData();
  res.json(sentimentData.currentSentiment);
});

app.get('/sentiment/history', (req, res) => {
  console.log('📈 Sentiment history requested');
  const sentimentData = generateMockSentimentData();
  res.json(sentimentData.historicalData);
});

app.get('/sentiment/sectors', (req, res) => {
  console.log('🏭 Sector sentiment requested');
  const sentimentData = generateMockSentimentData();
  res.json(sentimentData.sectorBreakdown);
});

// AI Research (mocked Gemini response)
app.post('/ai/research', (req, res) => {
  console.log('🤖 AI research requested:', req.body);
  const question = (req.body?.question || '').toString();
  const now = new Date().toISOString();
  const response = {
    executiveSummary: `Summary for: ${question || 'Indian markets'} — Bank NIFTY and key sectors show mixed momentum; outlook depends on rate trajectory and liquidity conditions.`,
    keyFindings: [
      { title: 'Momentum Check', detail: 'Short-term trend shows range-bound movement amid global cues.', impact: 'Neutral' },
      { title: 'Banking Flows', detail: 'Large-cap banks see steady inflows; PSU banks more volatile.', impact: 'Positive' },
      { title: 'Macro Risks', detail: 'Crude volatility and USD strength remain overhangs.', impact: 'Negative' }
    ],
    relatedTickers: ['HDFCBANK','ICICIBANK','SBIN'],
    sectors: ['Banking','IT'],
    riskFactors: ['Crude oil volatility','INR depreciation','Rate hike risk'],
    sources: [
      { name: 'Moneycontrol', url: 'https://www.moneycontrol.com/' },
      { name: 'The Economic Times', url: 'https://economictimes.indiatimes.com/' },
      { name: 'NSE', url: 'https://www.nseindia.com/' }
    ],
    timestamp: now
  };
  res.json(response);
});

// User watchlist API (Phase 3)
app.get('/users/:userId/watchlist', (req, res) => {
  console.log(`⭐ Watchlist requested for user: ${req.params.userId}`);
  const watchlist = [
    { id: '1', ticker: 'RELIANCE', addedAt: new Date().toISOString() },
    { id: '2', ticker: 'TCS', addedAt: new Date().toISOString() },
    { id: '3', ticker: 'HDFCBANK', addedAt: new Date().toISOString() }
  ];
  res.json(watchlist);
});

app.post('/users/:userId/watchlist', (req, res) => {
  console.log(`➕ Adding to watchlist for user: ${req.params.userId}`, req.body);
  const newItem = {
    id: Date.now().toString(),
    ticker: req.body.ticker,
    addedAt: new Date().toISOString()
  };
  res.json(newItem);
});

app.delete('/users/:userId/watchlist/:itemId', (req, res) => {
  console.log(`➖ Removing from watchlist: ${req.params.itemId}`);
  res.json({ success: true });
});

// Feedback API (Phase 3)
app.post('/feedback', (req, res) => {
  console.log('📝 Feedback submitted:', req.body);
  const feedback = {
    id: Date.now().toString(),
    ...req.body,
    submittedAt: new Date().toISOString()
  };
  res.json(feedback);
});

// Stock search API
app.get('/stocks/search', (req, res) => {
  const query = req.query.q?.toUpperCase() || '';
  console.log(`🔍 Stock search for: ${query}`);
  
  const stocks = [
    { ticker: 'RELIANCE', name: 'Reliance Industries', price: 2450.00, changePercent: 3.5 },
    { ticker: 'TCS', name: 'Tata Consultancy Services', price: 3200.00, changePercent: 2.8 },
    { ticker: 'HDFCBANK', name: 'HDFC Bank', price: 1650.00, changePercent: 2.1 },
    { ticker: 'INFY', name: 'Infosys', price: 1500.00, changePercent: -1.8 },
    { ticker: 'MARUTI', name: 'Maruti Suzuki', price: 12000.00, changePercent: 1.2 }
  ];
  
  const filteredStocks = stocks.filter(stock => 
    stock.ticker.includes(query) || stock.name.toLowerCase().includes(query.toLowerCase())
  );
  
  res.json(filteredStocks);
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Mock Backend Server running on http://localhost:${PORT}`);
  console.log(`📊 Market Data API: http://localhost:${PORT}/market-data`);
  console.log(`📰 News API: http://localhost:${PORT}/articles`);
  console.log(`🧠 Sentiment API: http://localhost:${PORT}/sentiment/current`);
  console.log(`⭐ Watchlist API: http://localhost:${PORT}/users/:userId/watchlist`);
  console.log(`📝 Feedback API: http://localhost:${PORT}/feedback`);
  console.log(`🔍 Stock Search: http://localhost:${PORT}/stocks/search?q=RELIANCE`);
});
