import React, { useState, useEffect } from 'react'
import NewsFeed from './components/NewsFeed'
import MarketOverview from './components/MarketOverview'
import SentimentHub from './components/SentimentHub'
import Watchlist from './components/Watchlist'
import HowItWorks from './components/HowItWorks'
import Contact from './components/Contact'
import Navbar from './components/Navbar'
import AIResearch from './components/AIResearch'
import apiService from './services/api'

function App() {
  const [currentPage, setCurrentPage] = useState('market')
  const [marketData, setMarketData] = useState(null)
  const [articles, setArticles] = useState([])
  const [sentimentData, setSentimentData] = useState(null)
  const [loading, setLoading] = useState(true)

  // Fetch data on component mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        
        // Fetch all data in parallel
        const [marketDataResult, articlesResult, sentimentResult] = await Promise.all([
          apiService.fetchMarketData(),
          apiService.fetchArticles(),
          apiService.fetchCurrentSentiment()
        ])

        setMarketData(marketDataResult)
        setArticles(articlesResult)
        setSentimentData(sentimentResult)
      } catch (error) {
        console.error('Error fetching data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  // Refresh data every 5 minutes
  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const [marketDataResult, articlesResult, sentimentResult] = await Promise.all([
          apiService.fetchMarketData(),
          apiService.fetchArticles(),
          apiService.fetchCurrentSentiment()
        ])

        setMarketData(marketDataResult)
        setArticles(articlesResult)
        setSentimentData(sentimentResult)
      } catch (error) {
        console.error('Error refreshing data:', error)
      }
    }, 5 * 60 * 1000) // 5 minutes

    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-400 mx-auto mb-4"></div>
          <p className="text-gray-300">Loading market data...</p>
        </div>
      </div>
    )
  }

  return (
    <>
      <Navbar currentPage={currentPage} onPageChange={setCurrentPage} />
      {currentPage === 'ai' && <AIResearch />} 
      {currentPage === 'news' && <NewsFeed articles={articles} />}
      {currentPage === 'market' && <MarketOverview marketData={marketData} />}
      {currentPage === 'sentiment' && <SentimentHub sentimentData={sentimentData} />}
      {currentPage === 'watchlist' && <Watchlist />}
      {currentPage === 'howitworks' && <HowItWorks />}
      {currentPage === 'contact' && <Contact />}
    </>
  )
}

export default App
