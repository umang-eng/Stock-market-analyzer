import React from 'react'

const MarketOverview = ({ marketData }) => {
  // Use real data if available, otherwise fallback to mock data
  const indices = marketData?.indices || [
    { name: 'NIFTY 50', price: 24150.75, change: 120.25, changePercent: 0.50 },
    { name: 'SENSEX', price: 78450.10, change: 400.50, changePercent: 0.51 }
  ]

  const gainers = marketData?.gainers || []
  const losers = marketData?.losers || []
  const sectors = marketData?.sectors || []

  const getSectorBgColor = (changePercent) => {
    if (changePercent > 1) return 'bg-green-700 hover:bg-green-600'
    if (changePercent > 0) return 'bg-green-500 hover:bg-green-400'
    if (changePercent < -1) return 'bg-red-700 hover:bg-red-600'
    if (changePercent < 0) return 'bg-red-500 hover:bg-red-400'
    return 'bg-slate-700 hover:bg-slate-600'
  }

  return (
    <div className="bg-slate-900 text-gray-200 font-sans min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-white text-3xl font-bold mb-8">Market Overview</h1>
        
        {/* Section 1: Index Performance */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {indices.map((index, idx) => (
            <div key={idx} className="bg-slate-800 rounded-lg shadow-lg p-6">
              <h3 className="text-white text-xl font-bold mb-4">{index.name}</h3>
              <div className="text-white text-2xl font-bold mb-2">
                {index.price.toLocaleString('en-IN', { maximumFractionDigits: 2 })}
              </div>
              <div className={`text-sm font-semibold ${
                index.changePercent >= 0 ? 'text-green-500' : 'text-red-500'
              }`}>
                {index.change >= 0 ? '+' : ''}{index.change.toFixed(2)} ({index.changePercent >= 0 ? '+' : ''}{index.changePercent.toFixed(2)}%)
              </div>
              
              {/* Simple SVG Chart */}
              <div className="mt-4">
                <svg viewBox="0 0 100 30" className="w-full h-8">
                  <path
                    d="M0 20 L20 10 L40 15 L60 5 L80 10 L100 20"
                    stroke={index.changePercent >= 0 ? "#10b981" : "#ef4444"}
                    strokeWidth="2"
                    fill="none"
                  />
                </svg>
              </div>
            </div>
          ))}
        </div>

        {/* Section 2: Market Movers */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Top Gainers */}
          <div className="bg-slate-800 rounded-lg shadow-lg p-6">
            <h3 className="text-white text-xl font-bold mb-4">Top Gainers</h3>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-slate-700">
                    <th className="text-left text-gray-400 py-2">Stock</th>
                    <th className="text-right text-gray-400 py-2">Price</th>
                    <th className="text-right text-gray-400 py-2">% Change</th>
                  </tr>
                </thead>
                <tbody>
                  {gainers.slice(0, 10).map((gainer, idx) => (
                    <tr key={idx} className="border-b border-slate-700">
                      <td className="py-2">
                        <div>
                          <div className="text-white font-semibold">{gainer.ticker}</div>
                          <div className="text-gray-400 text-sm">{gainer.name}</div>
                        </div>
                      </td>
                      <td className="text-right text-white font-medium py-2">
                        ₹{gainer.price.toLocaleString('en-IN', { maximumFractionDigits: 2 })}
                      </td>
                      <td className="text-right text-green-500 font-semibold py-2">
                        +{gainer.changePercent.toFixed(2)}%
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Top Losers */}
          <div className="bg-slate-800 rounded-lg shadow-lg p-6">
            <h3 className="text-white text-xl font-bold mb-4">Top Losers</h3>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-slate-700">
                    <th className="text-left text-gray-400 py-2">Stock</th>
                    <th className="text-right text-gray-400 py-2">Price</th>
                    <th className="text-right text-gray-400 py-2">% Change</th>
                  </tr>
                </thead>
                <tbody>
                  {losers.slice(0, 10).map((loser, idx) => (
                    <tr key={idx} className="border-b border-slate-700">
                      <td className="py-2">
                        <div>
                          <div className="text-white font-semibold">{loser.ticker}</div>
                          <div className="text-gray-400 text-sm">{loser.name}</div>
                        </div>
                      </td>
                      <td className="text-right text-white font-medium py-2">
                        ₹{loser.price.toLocaleString('en-IN', { maximumFractionDigits: 2 })}
                      </td>
                      <td className="text-right text-red-500 font-semibold py-2">
                        {loser.changePercent.toFixed(2)}%
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Section 3: Sector Performance Heatmap */}
        <div className="bg-slate-800 rounded-lg shadow-lg p-6">
          <h3 className="text-white text-xl font-bold mb-4">Sector Performance Heatmap</h3>
          <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2">
            {sectors.map((sector, idx) => (
              <div
                key={idx}
                className={`${getSectorBgColor(sector.changePercent)} rounded-md p-4 flex flex-col justify-end min-h-[100px] transition-colors`}
              >
                <div className="text-white font-semibold text-sm">{sector.name}</div>
                <div className="text-white text-sm mt-1">
                  {sector.changePercent >= 0 ? '+' : ''}{sector.changePercent.toFixed(1)}%
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Data Source Info */}
        {marketData && (
          <div className="mt-6 text-center text-gray-400 text-sm">
            Last updated: {new Date(marketData.lastUpdated).toLocaleString()}
          </div>
        )}
      </div>
    </div>
  )
}

export default MarketOverview
