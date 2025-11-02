import React, { useState } from 'react'

const NewsFeed = ({ articles }) => {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedSentiment, setSelectedSentiment] = useState('All Sentiments')
  const [selectedSector, setSelectedSector] = useState('All Sectors')
  const [selectedSource, setSelectedSource] = useState('All Sources')

  // Filter articles based on search and filters
  const filteredArticles = articles.filter(article => {
    const matchesSearch = article.headline.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         article.summary.toLowerCase().includes(searchTerm.toLowerCase())
    
    const matchesSentiment = selectedSentiment === 'All Sentiments' || 
                           article.sentiment === selectedSentiment
    
    const matchesSector = selectedSector === 'All Sectors' || 
                         article.sectors.includes(selectedSector)
    
    const matchesSource = selectedSource === 'All Sources' || 
                         article.source === selectedSource

    return matchesSearch && matchesSentiment && matchesSector && matchesSource
  })

  const getSentimentBadgeColor = (sentiment) => {
    switch (sentiment) {
      case 'Positive':
        return 'bg-green-800/50 text-green-300'
      case 'Negative':
        return 'bg-red-800/50 text-red-300'
      default:
        return 'bg-gray-800/50 text-gray-300'
    }
  }

  return (
    <div className="bg-slate-900 text-gray-200 font-sans min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-white text-3xl font-bold mb-8">Market News Feed</h1>
        
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Filter Sidebar */}
          <div className="lg:col-span-1">
            <div className="lg:sticky top-24">
              <div className="bg-slate-800 rounded-lg shadow-lg p-6">
                <h3 className="text-white text-xl font-bold mb-5">Filters</h3>
                
                <form className="flex flex-col gap-6">
                  {/* Search */}
                  <div>
                    <label htmlFor="search" className="block text-sm font-medium text-gray-300 mb-2">
                      Search Keywords
                    </label>
                    <input
                      type="text"
                      id="search"
                      placeholder="e.g., 'Reliance' or 'IPO'"
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="w-full bg-slate-700 text-white border-slate-600 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 px-3 py-2"
                    />
                  </div>

                  {/* AI Sentiment */}
                  <div>
                    <label htmlFor="sentiment" className="block text-sm font-medium text-gray-300 mb-2">
                      AI Sentiment
                    </label>
                    <select
                      id="sentiment"
                      value={selectedSentiment}
                      onChange={(e) => setSelectedSentiment(e.target.value)}
                      className="w-full bg-slate-700 text-white border-slate-600 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 px-3 py-2"
                    >
                      <option value="All Sentiments">All Sentiments</option>
                      <option value="Positive">Positive</option>
                      <option value="Negative">Negative</option>
                      <option value="Neutral">Neutral</option>
                    </select>
                  </div>

                  {/* Sector */}
                  <div>
                    <label htmlFor="sector" className="block text-sm font-medium text-gray-300 mb-2">
                      Sector
                    </label>
                    <select
                      id="sector"
                      value={selectedSector}
                      onChange={(e) => setSelectedSector(e.target.value)}
                      className="w-full bg-slate-700 text-white border-slate-600 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 px-3 py-2"
                    >
                      <option value="All Sectors">All Sectors</option>
                      <option value="IT">IT</option>
                      <option value="Banking">Banking</option>
                      <option value="Pharma">Pharma</option>
                      <option value="Auto">Auto</option>
                      <option value="FMCG">FMCG</option>
                      <option value="Energy">Energy</option>
                    </select>
                  </div>

                  {/* Source */}
                  <div>
                    <label htmlFor="source" className="block text-sm font-medium text-gray-300 mb-2">
                      Source
                    </label>
                    <select
                      id="source"
                      value={selectedSource}
                      onChange={(e) => setSelectedSource(e.target.value)}
                      className="w-full bg-slate-700 text-white border-slate-600 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 px-3 py-2"
                    >
                      <option value="All Sources">All Sources</option>
                      <option value="Moneycontrol">Moneycontrol</option>
                      <option value="The Economic Times">The Economic Times</option>
                      <option value="Livemint">Livemint</option>
                      <option value="Business Standard">Business Standard</option>
                    </select>
                  </div>

                  <button
                    type="button"
                    onClick={() => {
                      setSearchTerm('')
                      setSelectedSentiment('All Sentiments')
                      setSelectedSector('All Sectors')
                      setSelectedSource('All Sources')
                    }}
                    className="w-full py-2 px-4 bg-indigo-600 text-white font-semibold rounded-md shadow-md hover:bg-indigo-500 transition-colors"
                  >
                    Clear Filters
                  </button>
                </form>
              </div>
            </div>
          </div>

          {/* News Feed */}
          <div className="lg:col-span-3">
            <div className="flex flex-col gap-6">
              {filteredArticles.length > 0 ? (
                filteredArticles.map((article) => (
                  <div
                    key={article.id}
                    className="bg-slate-800 rounded-lg shadow-lg hover:bg-slate-700 transition-colors p-6"
                  >
                    <div className="flex justify-between items-start mb-3">
                      <span className="text-indigo-400 text-sm font-medium">
                        {article.source}
                      </span>
                      <span className={`px-2 py-1 rounded-full text-xs font-semibold ${getSentimentBadgeColor(article.sentiment)}`}>
                        {article.sentiment}
                      </span>
                    </div>
                    
                    <h2 className="text-white text-xl font-bold mb-3 leading-tight">
                      {article.headline}
                    </h2>
                    
                    <p className="text-gray-300 mb-4 leading-relaxed">
                      {article.summary}
                    </p>
                    
                    <div className="flex flex-wrap gap-2">
                      {article.tickers.map((ticker, idx) => (
                        <span
                          key={idx}
                          className="bg-slate-700 text-indigo-300 px-2 py-1 rounded text-xs font-medium"
                        >
                          {ticker}
                        </span>
                      ))}
                      {article.sectors.map((sector, idx) => (
                        <span
                          key={idx}
                          className="bg-slate-700 text-green-300 px-2 py-1 rounded text-xs font-medium"
                        >
                          {sector}
                        </span>
                      ))}
                    </div>
                    
                    <div className="mt-4 text-gray-400 text-sm">
                      {new Date(article.publishedAt).toLocaleString()}
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center py-12">
                  <p className="text-gray-400 text-lg">No articles found matching your filters.</p>
                  <p className="text-gray-500 text-sm mt-2">Try adjusting your search criteria.</p>
                </div>
              )}
            </div>

            {/* Load More Button */}
            <div className="mt-8">
              <button className="w-full text-center py-3 px-6 bg-slate-800 text-indigo-400 font-semibold rounded-lg shadow-md hover:bg-slate-700 transition-colors cursor-pointer">
                Load More Articles
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default NewsFeed
