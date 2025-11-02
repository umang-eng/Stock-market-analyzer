import React, { useState } from 'react'

const Watchlist = () => {
  const [addStockInput, setAddStockInput] = useState('')

  const watchedStocks = [
    { ticker: 'TCS', name: 'Tata Consultancy', price: '4,150.20', change: '+1.2%', changeType: 'positive' },
    { ticker: 'HDFCBANK', name: 'HDFC Bank', price: '1,675.40', change: '-0.5%', changeType: 'negative' },
    { ticker: 'RELIANCE', name: 'Reliance Industries', price: '2,456.75', change: '+0.8%', changeType: 'positive' },
    { ticker: 'INFY', name: 'Infosys', price: '1,842.60', change: '0.0%', changeType: 'neutral' }
  ]

  const handleAddStock = (e) => {
    e.preventDefault()
    console.log('Adding stock:', addStockInput)
    setAddStockInput('')
  }

  const handleRemoveStock = (ticker) => {
    console.log('Removing stock:', ticker)
  }

  const personalizedNews = [
    {
      source: 'Business Standard',
      sentiment: 'Positive',
      sentimentStyle: 'bg-green-800/50 text-green-300',
      headline: 'TCS Wins $500M Multi-Year Contract from US Client',
      summary: 'AI Analysis: Tata Consultancy Services secures major IT services contract, expected to boost revenues by $500M over 5 years. Positive impact on long-term outlook. Stock price up 1.2% in pre-market trading.'
    },
    {
      source: 'Economic Times',
      sentiment: 'Positive',
      sentimentStyle: 'bg-green-800/50 text-green-300',
      headline: 'HDFC Bank Reports Strong Growth in SME Lending',
      summary: 'AI Analysis: Small and medium enterprise loan book expanded 18% year-over-year. Digital banking initiatives showing positive results. Management remains optimistic about credit quality.'
    },
    {
      source: 'Moneycontrol',
      sentiment: 'Positive',
      sentimentStyle: 'bg-green-800/50 text-green-300',
      headline: 'Reliance Jio Launches 5G Services in 500 Cities',
      summary: 'AI Analysis: Rapid rollout of 5G infrastructure continues. User adoption rate exceeds expectations. Telecommunication segment showing strong momentum for next quarter.'
    },
    {
      source: 'Livemint',
      sentiment: 'Negative',
      sentimentStyle: 'bg-red-800/50 text-red-300',
      headline: 'Infosys Faces Margin Pressure from Wage Hikes',
      summary: 'AI Analysis: Annual wage increases expected to impact Q4 margins by 1-1.5%. Despite strong revenue growth, profitability concerns emerge. Analysts downgrade price targets.'
    },
    {
      source: 'Business Standard',
      sentiment: 'Positive',
      sentimentStyle: 'bg-green-800/50 text-green-300',
      headline: 'RELIANCE Announces Major Green Energy Investment',
      summary: 'AI Analysis: Company commits $10 billion to renewable energy projects over next 3 years. Strategic pivot aligns with global sustainability trends. Positive long-term outlook.'
    }
  ]

  return (
    <div className="bg-slate-900 text-gray-200 font-sans min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Page Title */}
        <h1 className="text-white text-3xl font-bold mb-8">My Watchlist</h1>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          
          {/* Section 1: My Followed Stocks Sidebar */}
          <div className="lg:col-span-1">
            <div className="lg:sticky lg:top-24">
              <div className="bg-slate-800 rounded-lg shadow-lg p-6">
                
                {/* Component A: Add Stock Form */}
                <form onSubmit={handleAddStock}>
                  <label htmlFor="add_stock" className="block text-sm font-medium text-gray-300 mb-2">
                    Add Stock
                  </label>
                  <input
                    type="search"
                    id="add_stock"
                    value={addStockInput}
                    onChange={(e) => setAddStockInput(e.target.value)}
                    placeholder="Search to add stock..."
                    className="w-full px-3 py-2 bg-slate-700 text-white border border-slate-600 rounded-md shadow-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                  />
                </form>

                {/* Component B: Stock List */}
                <div className="border-t border-slate-700 my-6"></div>
                
                <div className="space-y-4">
                  {watchedStocks.map((stock, index) => (
                    <div key={index} className="flex items-center justify-between gap-2">
                      <div className="flex-1 flex flex-col">
                        <span className="text-white font-bold text-lg">{stock.ticker}</span>
                        <span className="text-gray-400 text-sm">{stock.name}</span>
                      </div>
                      
                      <div className="flex items-center gap-2">
                        <div className="text-right flex flex-col">
                          <span className="text-white font-medium">{stock.price}</span>
                          <span className={`text-sm font-semibold ${
                            stock.changeType === 'positive' ? 'text-green-500' :
                            stock.changeType === 'negative' ? 'text-red-500' :
                            'text-gray-400'
                          }`}>
                            {stock.change}
                          </span>
                        </div>
                        
                        <button
                          onClick={() => handleRemoveStock(stock.ticker)}
                          className="p-1 text-gray-500 hover:text-red-400 transition-colors"
                          aria-label={`Remove ${stock.ticker}`}
                        >
                          <svg 
                            xmlns="http://www.w3.org/2000/svg" 
                            fill="none" 
                            viewBox="0 0 24 24" 
                            strokeWidth="2" 
                            stroke="currentColor" 
                            className="w-4 h-4"
                          >
                            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                          </svg>
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Section 2: Personalized News Feed */}
          <div className="lg:col-span-3">
            <h2 className="text-white text-2xl font-bold mb-6">Your Personalized News</h2>
            
            <div className="flex flex-col gap-6">
              
              {/* News Cards */}
              {personalizedNews.map((article, index) => (
                <div 
                  key={index}
                  className="bg-slate-800 rounded-lg shadow-lg hover:bg-slate-700 transition p-5"
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-indigo-400 text-sm font-semibold">
                      {article.source}
                    </span>
                    <span className={`${article.sentimentStyle} text-xs px-2 py-1 rounded-full font-medium`}>
                      {article.sentiment}
                    </span>
                  </div>
                  <h3 className="text-white font-bold text-lg mb-2">
                    {article.headline}
                  </h3>
                  <p className="text-gray-300 text-sm leading-relaxed">
                    {article.summary}
                  </p>
                </div>
              ))}

              {/* Load More Button */}
              <button 
                className="w-full text-center py-3 px-6 bg-slate-800 text-indigo-400 font-semibold rounded-lg shadow-md hover:bg-slate-700 transition-colors cursor-pointer border border-indigo-400/30"
              >
                Load More Articles
              </button>

            </div>
          </div>

        </div>
      </div>
    </div>
  )
}

export default Watchlist
