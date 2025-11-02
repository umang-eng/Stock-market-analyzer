# ⚡ Quick Start Guide

Get the Fintech AI News Platform running locally in 5 minutes!

## Prerequisites

- Node.js 18+ installed
- npm installed
- Terminal access

## Local Setup (3 Steps)

### 1. Install Dependencies

```bash
# Install frontend dependencies
npm install

# Install mock backend dependencies
cd mock-backend
npm install
cd ..
```

### 2. Start Mock Backend

Open Terminal 1:

```bash
cd mock-backend
node server.js
```

You should see:
```
🚀 Mock Backend Server running on http://localhost:3001
Mock API endpoints ready:
- GET  /market-data
- GET  /articles
- GET  /current-sentiment
- GET  /sentiment-history
- POST /ai/research
- POST /feedback
```

### 3. Start Frontend

Open Terminal 2:

```bash
npm run dev
```

You should see:
```
VITE v5.0.8  ready in XXX ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

## 🎉 You're Ready!

Open your browser and navigate to:
**http://localhost:5173**

## 📱 Test the Pages

1. **Market Overview** (`/`) - View indices, gainers, losers
2. **All News** - Browse AI-analyzed news
3. **Sentiment Hub** - Market sentiment trends
4. **My Watchlist** - Personal stock tracking
5. **AI Research** - Ask AI questions about stocks
6. **How It Works** - Platform explanation
7. **Contact** - Submit feedback

## 🔧 Troubleshooting

### Port Already in Use

If port 3001 is taken by the mock backend:
```bash
# Kill the process
lsof -ti:3001 | xargs kill -9
```

If port 5173 is taken by Vite:
```bash
# Kill the process
lsof -ti:5173 | xargs kill -9
```

### Frontend Shows Blank Page

1. Check if mock backend is running: `curl http://localhost:3001/health`
2. Check browser console for errors (F12)
3. Clear browser cache and hard refresh (Cmd+Shift+R)

### "Cannot find module" Error

Reinstall dependencies:
```bash
rm -rf node_modules package-lock.json
npm install
```

## 🚀 Next Steps

- Read [README.md](./README.md) for full documentation
- Check [DEPLOYMENT.md](./DEPLOYMENT.md) to deploy to cloud
- Review [CONTRIBUTING.md](./CONTRIBUTING.md) to contribute

## 💡 Development Tips

### Running Both at Once

Create a `dev.sh` script:
```bash
#!/bin/bash
cd mock-backend && node server.js &
BACKEND_PID=$!
cd .. && npm run dev
kill $BACKEND_PID
```

Make it executable:
```bash
chmod +x dev.sh
./dev.sh
```

### Mock Data

All data is currently mock data. To use real data:
1. Follow [DEPLOYMENT.md](./DEPLOYMENT.md)
2. Deploy Cloud Functions
3. Update `.env` with production API URL

## 📞 Need Help?

- Check the [Issues](https://github.com/yourusername/fintech-ai-news/issues) page
- Read the full [README.md](./README.md)
- Contact: [Your Email]

Happy Coding! 🎉

