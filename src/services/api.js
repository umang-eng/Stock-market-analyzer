// API service for connecting frontend to mock backend

const API_BASE_URL = 'http://localhost:3001';

class ApiService {

  async researchAI(question) {
    try {
      const base = import.meta?.env?.VITE_AI_API_URL || 'http://localhost:3001';
      const resp = await fetch(`${base}/ai/research`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });
      if (!resp.ok) throw new Error('AI research API error');
      return await resp.json();
    } catch (e) {
      console.error('AI research error:', e);
      return null;
    }
  }
  async fetchMarketData() {
    try {
      const response = await fetch(`${API_BASE_URL}/market-data`);
      if (!response.ok) throw new Error('Failed to fetch market data');
      return await response.json();
    } catch (error) {
      console.error('Error fetching market data:', error);
      return null;
    }
  }

  async fetchArticles() {
    try {
      const response = await fetch(`${API_BASE_URL}/articles`);
      if (!response.ok) throw new Error('Failed to fetch articles');
      return await response.json();
    } catch (error) {
      console.error('Error fetching articles:', error);
      return [];
    }
  }

  async fetchCurrentSentiment() {
    try {
      const response = await fetch(`${API_BASE_URL}/sentiment/current`);
      if (!response.ok) throw new Error('Failed to fetch sentiment');
      return await response.json();
    } catch (error) {
      console.error('Error fetching sentiment:', error);
      return { averageScore: 0, articlesAnalyzed: 0 };
    }
  }

  async fetchSentimentHistory() {
    try {
      const response = await fetch(`${API_BASE_URL}/sentiment/history`);
      if (!response.ok) throw new Error('Failed to fetch sentiment history');
      return await response.json();
    } catch (error) {
      console.error('Error fetching sentiment history:', error);
      return [];
    }
  }

  async fetchSectorSentiment() {
    try {
      const response = await fetch(`${API_BASE_URL}/sentiment/sectors`);
      if (!response.ok) throw new Error('Failed to fetch sector sentiment');
      return await response.json();
    } catch (error) {
      console.error('Error fetching sector sentiment:', error);
      return {};
    }
  }

  async fetchWatchlist(userId) {
    try {
      const response = await fetch(`${API_BASE_URL}/users/${userId}/watchlist`);
      if (!response.ok) throw new Error('Failed to fetch watchlist');
      return await response.json();
    } catch (error) {
      console.error('Error fetching watchlist:', error);
      return [];
    }
  }

  async addToWatchlist(userId, ticker) {
    try {
      const response = await fetch(`${API_BASE_URL}/users/${userId}/watchlist`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticker })
      });
      if (!response.ok) throw new Error('Failed to add to watchlist');
      return await response.json();
    } catch (error) {
      console.error('Error adding to watchlist:', error);
      return null;
    }
  }

  async removeFromWatchlist(userId, itemId) {
    try {
      const response = await fetch(`${API_BASE_URL}/users/${userId}/watchlist/${itemId}`, {
        method: 'DELETE'
      });
      if (!response.ok) throw new Error('Failed to remove from watchlist');
      return true;
    } catch (error) {
      console.error('Error removing from watchlist:', error);
      return false;
    }
  }

  async submitFeedback(feedbackData) {
    try {
      const response = await fetch(`${API_BASE_URL}/feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(feedbackData)
      });
      if (!response.ok) throw new Error('Failed to submit feedback');
      return await response.json();
    } catch (error) {
      console.error('Error submitting feedback:', error);
      return null;
    }
  }

  async searchStocks(query) {
    try {
      const response = await fetch(`${API_BASE_URL}/stocks/search?q=${encodeURIComponent(query)}`);
      if (!response.ok) throw new Error('Failed to search stocks');
      return await response.json();
    } catch (error) {
      console.error('Error searching stocks:', error);
      return [];
    }
  }
}

export default new ApiService();
