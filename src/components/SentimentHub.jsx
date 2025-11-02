import React, { useState } from 'react'

const SentimentHub = () => {
  const [activeFilter, setActiveFilter] = useState('30D')
  const [stockSearch, setStockSearch] = useState('')

  const handleStockSearch = (e) => {
    e.preventDefault()
    console.log('Searching for:', stockSearch)
  }

  return (
    <div className="bg-slate-900 text-gray-200 font-sans min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Page Title */}
        <h1 className="text-white text-3xl font-bold mb-8">AI Sentiment Hub</h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Section 1: Overall Market Sentiment Trend */}
          <div className="lg:col-span-2">
            <div className="bg-slate-800 rounded-lg shadow-lg p-6 mb-8">
              {/* Header */}
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-white text-xl font-bold">Overall Market Sentiment Trend</h3>
                <div className="flex gap-2">
                  {['7D', '30D', '6M'].map((filter) => (
                    <button
                      key={filter}
                      onClick={() => setActiveFilter(filter)}
                      className={`py-1 px-3 rounded-md text-sm transition-colors ${
                        activeFilter === filter
                          ? 'bg-indigo-600 text-white'
                          : 'bg-slate-700 text-gray-300 hover:bg-slate-600'
                      }`}
                    >
                      {filter}
                    </button>
                  ))}
                </div>
              </div>

              {/* Chart */}
              <div className="mt-6" style={{ height: '300px' }}>
                <svg viewBox="0 0 100 50" preserveAspectRatio="none" className="w-full h-full">
                  {/* Y-axis labels */}
                  <text x="2" y="10" fill="#9ca3af" fontSize="3" className="fill-gray-400">
                    Greed
                  </text>
                  <text x="2" y="30" fill="#9ca3af" fontSize="3" className="fill-gray-400">
                    Neutral
                  </text>
                  <text x="2" y="48" fill="#9ca3af" fontSize="3" className="fill-gray-400">
                    Fear
                  </text>

                  {/* Y-axis reference lines */}
                  <line x1="0" y1="10" x2="100" y2="10" stroke="#374151" strokeWidth="0.5" strokeDasharray="1" />
                  <line x1="0" y1="30" x2="100" y2="30" stroke="#374151" strokeWidth="0.5" strokeDasharray="1" />
                  <line x1="0" y1="48" x2="100" y2="48" stroke="#374151" strokeWidth="0.5" strokeDasharray="1" />

                  {/* X-axis */}
                  <line x1="0" y1="48" x2="100" y2="48" stroke="#9ca3af" strokeWidth="0.5" />

                  {/* Main trend line (indicating gradually improving sentiment) */}
                  <path
                    d="M0 25 L10 23 L20 21 L30 19 L40 17 L50 16 L60 15 L70 14 L80 13 L90 13 L100 12"
                    stroke="#818cf8"
                    strokeWidth="0.8"
                    fill="none"
                  />

                  {/* Area fill under the line */}
                  <path
                    d="M0 48 L0 25 L10 23 L20 21 L30 19 L40 17 L50 16 L60 15 L70 14 L80 13 L90 13 L100 12 L100 48 Z"
                    fill="url(#gradient)"
                    opacity="0.2"
                  />

                  {/* Gradient definition */}
                  <defs>
                    <linearGradient id="gradient" x1="0%" y1="0%" x2="0%" y2="100%">
                      <stop offset="0%" stopColor="#818cf8" />
                      <stop offset="100%" stopColor="#818cf8" stopOpacity="0" />
                    </linearGradient>
                  </defs>
                </svg>
              </div>
            </div>

            {/* Section 2: Sentiment by Sector */}
            <div className="bg-slate-800 rounded-lg shadow-lg p-6">
              <h3 className="text-white text-xl font-bold mb-6">Sentiment by Sector (Last 24h)</h3>
              
              <div className="space-y-4">
                {/* IT */}
                <div className="flex items-center gap-4">
                  <span className="w-1/4 text-gray-300 font-medium">IT</span>
                  <div className="w-3/4 bg-slate-700 rounded-full h-2.5">
                    <div className="h-2.5 rounded-full bg-green-500" style={{ width: '75%' }}></div>
                  </div>
                </div>

                {/* Banking */}
                <div className="flex items-center gap-4">
                  <span className="w-1/4 text-gray-300 font-medium">Banking</span>
                  <div className="w-3/4 bg-slate-700 rounded-full h-2.5">
                    <div className="h-2.5 rounded-full bg-red-500" style={{ width: '40%' }}></div>
                  </div>
                </div>

                {/* Pharma */}
                <div className="flex items-center gap-4">
                  <span className="w-1/4 text-gray-300 font-medium">Pharma</span>
                  <div className="w-3/4 bg-slate-700 rounded-full h-2.5">
                    <div className="h-2.5 rounded-full bg-yellow-500" style={{ width: '50%' }}></div>
                  </div>
                </div>

                {/* Auto */}
                <div className="flex items-center gap-4">
                  <span className="w-1/4 text-gray-300 font-medium">Auto</span>
                  <div className="w-3/4 bg-slate-700 rounded-full h-2.5">
                    <div className="h-2.5 rounded-full bg-green-400" style={{ width: '67%' }}></div>
                  </div>
                </div>

                {/* FMCG */}
                <div className="flex items-center gap-4">
                  <span className="w-1/4 text-gray-300 font-medium">FMCG</span>
                  <div className="w-3/4 bg-slate-700 rounded-full h-2.5">
                    <div className="h-2.5 rounded-full bg-red-400" style={{ width: '33%' }}></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Section 3: Stock-Specific Deep Dive */}
          <div className="lg:col-span-1">
            <div className="lg:sticky lg:top-24">
              <div className="bg-slate-800 rounded-lg shadow-lg p-6">
                <h3 className="text-white text-xl font-bold mb-5">Stock-Specific Analysis</h3>
                
                {/* Search Box */}
                <form onSubmit={handleStockSearch}>
                  <label htmlFor="stock_search" className="sr-only">Search Stock</label>
                  <input
                    type="search"
                    id="stock_search"
                    value={stockSearch}
                    onChange={(e) => setStockSearch(e.target.value)}
                    placeholder="Search stock (e.g., 'RELIANCE')"
                    className="w-full px-3 py-2 bg-slate-700 text-white border border-slate-600 rounded-md shadow-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                  />
                </form>

                {/* Mocked Result Area */}
                <div className="mt-6">
                  <div className="border-t border-slate-700 my-6"></div>
                  <h4 className="text-white text-lg font-bold">Reliance Industries (RELIANCE)</h4>
                  
                  {/* Gauge */}
                  <div className="mt-4">
                    <svg viewBox="0 0 200 120" className="w-3/4 mx-auto" style={{ maxHeight: '150px' }}>
                      <path d="M 30 100 A 70 70 0 0 1 170 100" fill="none" stroke="#334155" strokeWidth="16" strokeLinecap="round"/>
                      <path d="M 30 100 A 70 70 0 0 1 100 65" fill="none" stroke="#10b981" strokeWidth="16" strokeLinecap="round"/>
                      <path d="M 100 65 A 70 70 0 0 1 100 35" fill="none" stroke="#eab308" strokeWidth="16" strokeLinecap="round"/>
                      <path d="M 100 35 A 70 70 0 0 1 170 100" fill="none" stroke="#ef4444" strokeWidth="16" strokeLinecap="round"/>
                      <g transform="translate(100, 100)">
                        <line x1="0" y1="0" x2="0" y2="-65" stroke="#ffffff" strokeWidth="3" strokeLinecap="round" transform="rotate(-25)"/>
                        <circle cx="0" cy="0" r="5" fill="#ffffff"/>
                      </g>
                      <text x="30" y="115" fill="#ef4444" fontSize="12" fontWeight="600">Negative</text>
                      <text x="88" y="28" fill="#eab308" fontSize="12" fontWeight="600">Neutral</text>
                      <text x="160" y="115" fill="#10b981" fontSize="12" fontWeight="600">Positive</text>
                    </svg>
                  </div>
                  <div className="text-green-400 text-xl font-bold text-center mt-2">Positive</div>

                  {/* Recent News */}
                  <h5 className="text-gray-300 font-semibold mt-6 mb-4">Recent AI-Analyzed News</h5>
                  
                  <div className="space-y-4">
                    {/* News Card 1 */}
                    <div className="bg-slate-700 rounded-lg p-4 hover:bg-slate-600 transition">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-indigo-400 text-xs font-semibold">Moneycontrol</span>
                        <span className="bg-green-800/50 text-green-300 text-xs px-2 py-1 rounded-full">Positive</span>
                      </div>
                      <h6 className="text-white font-bold text-sm mb-1">Strong Q4 Results Beat Expectations</h6>
                      <p className="text-gray-300 text-xs leading-relaxed">
                        Revenue up 18% driven by retail and digital services. Positive outlook maintained.
                      </p>
                    </div>

                    {/* News Card 2 */}
                    <div className="bg-slate-700 rounded-lg p-4 hover:bg-slate-600 transition">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-indigo-400 text-xs font-semibold">Economic Times</span>
                        <span className="bg-green-800/50 text-green-300 text-xs px-2 py-1 rounded-full">Positive</span>
                      </div>
                      <h6 className="text-white font-bold text-sm mb-1">Expansion Plans Announced</h6>
                      <p className="text-gray-300 text-xs leading-relaxed">
                        Major investments in renewable energy and telecommunications sectors underway.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  )
}

export default SentimentHub
