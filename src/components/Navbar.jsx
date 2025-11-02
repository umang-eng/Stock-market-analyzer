import React from 'react'

const Navbar = ({ currentPage, onPageChange }) => {
  const navigation = [
    { id: 'ai', name: 'AI', icon: '🤖' },
    { id: 'market', name: 'Market Overview', icon: '📊' },
    { id: 'news', name: 'All News', icon: '📰' },
    { id: 'sentiment', name: 'Sentiment Hub', icon: '🔍' },
    { id: 'watchlist', name: 'My Watchlist', icon: '⭐' },
    { id: 'howitworks', name: 'How It Works', icon: '💡' },
    { id: 'contact', name: 'Contact', icon: '✉️' },
  ]

  return (
    <nav className="bg-slate-800 shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div 
            onClick={() => onPageChange('market')}
            className="flex items-center cursor-pointer"
          >
            <span className="text-indigo-400 text-2xl font-bold">AI Market Insights</span>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex md:space-x-1">
            {navigation.map((item) => (
              <button
                key={item.id}
                onClick={() => onPageChange(item.id)}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  currentPage === item.id
                    ? 'bg-indigo-600 text-white'
                    : 'text-gray-300 hover:bg-slate-700 hover:text-white'
                }`}
              >
                <span className="mr-2">{item.icon}</span>
                {item.name}
              </button>
            ))}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => {
              const menu = document.getElementById('mobile-menu')
              menu.classList.toggle('hidden')
            }}
            className="md:hidden text-gray-300 hover:text-white p-2"
          >
            <svg
              className="h-6 w-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile Navigation Menu */}
      <div id="mobile-menu" className="hidden md:hidden">
        <div className="px-2 pt-2 pb-3 space-y-1 bg-slate-800 border-t border-slate-700">
          {navigation.map((item) => (
            <button
              key={item.id}
              onClick={() => {
                onPageChange(item.id)
                document.getElementById('mobile-menu').classList.add('hidden')
              }}
              className={`w-full text-left px-3 py-2 rounded-md text-base font-medium transition-colors ${
                currentPage === item.id
                  ? 'bg-indigo-600 text-white'
                  : 'text-gray-300 hover:bg-slate-700 hover:text-white'
              }`}
            >
              <span className="mr-2">{item.icon}</span>
              {item.name}
            </button>
          ))}
        </div>
      </div>
    </nav>
  )
}

export default Navbar
