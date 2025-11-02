"""
Configuration for different financial data API providers
"""

# Alpha Vantage Configuration
ALPHA_VANTAGE_CONFIG = {
    "base_url": "https://www.alphavantage.co/query",
    "functions": {
        "quote": "GLOBAL_QUOTE",
        "gainers": "TOP_GAINERS_LOSERS",
        "sectors": "SECTOR"
    }
}

# Finnhub Configuration
FINNHUB_CONFIG = {
    "base_url": "https://finnhub.io/api/v1",
    "functions": {
        "quote": "quote",
        "gainers": "stock/market-status",
        "sectors": "stock/sector-performance"
    }
}

# NSE India Configuration (if using direct NSE APIs)
NSE_CONFIG = {
    "base_url": "https://www.nseindia.com/api",
    "endpoints": {
        "indices": "/marketStatus",
        "gainers": "/equity-stockIndices",
        "losers": "/equity-stockIndices"
    }
}

# Indian Stock Symbols
INDIAN_INDICES = {
    "NIFTY_50": "^NSEI",
    "SENSEX": "^BSESN",
    "NIFTY_BANK": "^NSEBANK",
    "NIFTY_IT": "^CNXIT"
}

# Major Indian Stocks
MAJOR_STOCKS = [
    "RELIANCE.BSE",  # Reliance Industries
    "TCS.BSE",       # Tata Consultancy Services
    "HDFCBANK.BSE",  # HDFC Bank
    "INFY.BSE",      # Infosys
    "HINDUNILVR.BSE", # Hindustan Unilever
    "ICICIBANK.BSE", # ICICI Bank
    "KOTAKBANK.BSE", # Kotak Mahindra Bank
    "BHARTIARTL.BSE", # Bharti Airtel
    "SBIN.BSE",      # State Bank of India
    "LT.BSE"         # Larsen & Toubro
]

# Sector Mapping
SECTOR_MAPPING = {
    "IT": ["TCS", "INFY", "WIPRO", "HCLTECH"],
    "Banking": ["HDFCBANK", "ICICIBANK", "KOTAKBANK", "SBIN"],
    "Pharma": ["SUNPHARMA", "DRREDDY", "CIPLA", "BIOCON"],
    "Auto": ["MARUTI", "TATAMOTORS", "M&M", "BAJAJ-AUTO"],
    "FMCG": ["HINDUNILVR", "ITC", "NESTLEIND", "DABUR"],
    "Energy": ["RELIANCE", "ONGC", "GAIL", "BPCL"],
    "Metals": ["TATASTEEL", "JSWSTEEL", "HINDALCO", "SAIL"],
    "Real Estate": ["DLF", "GODREJPROP", "BRIGADE", "SOBHA"]
}
