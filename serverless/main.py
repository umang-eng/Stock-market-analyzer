"""
AI Market Insights - News Fetching & Analysis Cloud Function
Automatically fetches, analyzes, and stores Indian stock market news
"""

import json
import logging
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import functions_v2
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Firebase
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app()
db = firestore.client()

# Configure Gemini
genai.configure(api_key="YOUR_GEMINI_API_KEY")  # Set this in environment variables


class NewsPipeline:
    """Main pipeline for fetching and analyzing news articles"""
    
    # Top Indian financial news sources
    NEWS_SOURCES = [
        "site:moneycontrol.com",
        "site:economictimes.indiatimes.com",
        "site:livemint.com",
        "site:business-standard.com",
        "site:financialexpress.com",
        "site:thehindubusinessline.com",
    ]
    
    def __init__(self):
        self.model = genai.GenerativeModel(
            'gemini-2.0-flash-exp',
            tools=[{"google_search": {}}]
        )
        self.analysis_model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
    def _build_search_query(self) -> str:
        """Build a Google Search query for recent articles"""
        time_window = "15 minutes ago"
        
        sources_query = " OR ".join([f'"{src}"' for src in self.NEWS_SOURCES])
        
        query = f"""
        Find recent Indian stock market news articles published in the last 15-20 minutes from these sources:
        {sources_query}
        
        Return the article URLs and headlines for articles about:
        - Stock market news
        - Company earnings and results
        - Economic indicators
        - Sector-specific news (banking, IT, pharma, auto, etc.)
        - Corporate announcements
        - Market analysis and trends
        - IPOs and listings
        
        Provide only recent articles published within the last 15-20 minutes.
        Format the response as a JSON array with objects containing 'url' and 'headline' fields.
        """
        
        return query
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def fetch_recent_articles(self) -> List[Dict[str, str]]:
        """
        Fetch recent articles using Gemini with Google Search grounding
        Returns a list of {url, headline} dictionaries
        """
        try:
            logger.info("Fetching recent articles from Indian financial news sources...")
            
            query = self._build_search_query()
            
            response = self.model.generate_content(
                query,
                generation_config={
                    "temperature": 0.3,
                    "max_output_tokens": 2048,
                }
            )
            
            # Parse response
            articles = self._parse_search_response(response.text)
            
            logger.info(f"Fetched {len(articles)} articles from search")
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching articles: {str(e)}")
            raise
    
    def _parse_search_response(self, response_text: str) -> List[Dict[str, str]]:
        """Parse Gemini's response to extract URLs and headlines"""
        articles = []
        
        try:
            # Try to parse as JSON
            # Extract JSON from markdown code blocks if present
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(1)
            
            # Clean up the response
            response_text = response_text.strip()
            
            # Parse JSON
            data = json.loads(response_text)
            
            if isinstance(data, list):
                for item in data:
                    if 'url' in item and 'headline' in item:
                        articles.append({
                            'url': item['url'],
                            'headline': item['headline']
                        })
            
        except json.JSONDecodeError:
            logger.warning("Failed to parse response as JSON, attempting regex extraction")
            # Fallback: extract URLs using regex
            url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
            urls = re.findall(url_pattern, response_text)
            
            for url in urls:
                # Skip URLs that don't match our sources
                if any(source.replace('site:', '') in url for source in self.NEWS_SOURCES):
                    articles.append({
                        'url': url,
                        'headline': ''
                    })
        
        return articles
    
    def check_duplicate(self, url: str) -> bool:
        """Check if an article with this URL already exists in Firestore"""
        try:
            articles_ref = db.collection('articles')
            query = articles_ref.where('url', '==', url).limit(1)
            docs = query.stream()
            
            exists = any(True for _ in docs)
            return exists
            
        except Exception as e:
            logger.error(f"Error checking duplicate for {url}: {str(e)}")
            return False  # If error, skip rather than crash
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def analyze_article(self, url: str, headline: str) -> Optional[Dict[str, Any]]:
        """
        Analyze a single article using Gemini in JSON mode
        Returns the analysis as a dictionary matching our schema
        """
        try:
            logger.info(f"Analyzing article: {headline}")
            
            schema = {
                "type": "OBJECT",
                "properties": {
                    "headline": {"type": "STRING"},
                    "source": {
                        "type": "STRING",
                        "description": "The common name of the news source, e.g., 'The Economic Times'"
                    },
                    "url": {"type": "STRING"},
                    "summary": {
                        "type": "STRING",
                        "description": "A concise 1-2 sentence AI summary of the key impact."
                    },
                    "sentiment": {
                        "type": "STRING",
                        "enum": ["Positive", "Negative", "Neutral"]
                    },
                    "tickers": {
                        "type": "ARRAY",
                        "items": {"type": "STRING"},
                        "description": "A list of relevant Indian stock tickers, e.g., ['RELIANCE', 'TCS']. Use uppercase. Provide an empty array if none."
                    }
                },
                "required": ["headline", "source", "url", "summary", "sentiment", "tickers"]
            }
            
            prompt = f"""
            Analyze the content of this article:
            URL: {url}
            Headline: {headline}
            
            Please fetch and read the full article content from the URL, then provide a comprehensive analysis.
            
            Return ONLY a valid JSON object with the following structure:
            - headline: Extract or use the article's headline
            - source: The common name of the news source (e.g., "Moneycontrol", "The Economic Times")
            - url: The article URL
            - summary: A concise 1-2 sentence summary highlighting the key financial/economic impact
            - sentiment: One of "Positive", "Negative", or "Neutral" based on the impact on markets/stocks
            - tickers: Array of relevant Indian stock ticker symbols in UPPERCASE (e.g., ["RELIANCE", "TCS"]). Empty array [] if none apply.
            
            Focus on:
            1. Clear identification of affected companies/sectors
            2. Impact assessment (positive/negative/neutral)
            3. Key facts that would influence market decisions
            
            Return ONLY JSON, no additional text or explanation.
            """
            
            response = self.analysis_model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.2,
                    "response_mime_type": "application/json",
                    "response_schema": schema,
                }
            )
            
            # Parse and validate JSON response
            analysis = json.loads(response.text)
            
            # Validate required fields
            required_fields = ["headline", "source", "url", "summary", "sentiment", "tickers"]
            for field in required_fields:
                if field not in analysis:
                    logger.error(f"Missing required field '{field}' in analysis")
                    return None
            
            # Ensure sentiment is valid
            if analysis["sentiment"] not in ["Positive", "Negative", "Neutral"]:
                logger.warning(f"Invalid sentiment '{analysis['sentiment']}', defaulting to 'Neutral'")
                analysis["sentiment"] = "Neutral"
            
            logger.info(f"Successfully analyzed article: {analysis.get('headline', url)}")
            return analysis
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response for {url}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error analyzing article {url}: {str(e)}")
            return None
    
    def save_to_firestore(self, analysis: Dict[str, Any]) -> bool:
        """Save the analyzed article to Firestore"""
        try:
            article_data = {
                **analysis,
                "publishedAt": firestore.SERVER_TIMESTAMP,
                "processedAt": firestore.SERVER_TIMESTAMP,
            }
            
            # Add document to Firestore
            db.collection('articles').add(article_data)
            
            logger.info(f"Saved article to Firestore: {analysis.get('headline')}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving to Firestore: {str(e)}")
            return False
    
    def run(self) -> Dict[str, Any]:
        """
        Main pipeline execution
        Returns statistics about the run
        """
        stats = {
            "fetched": 0,
            "new_articles": 0,
            "analyzed": 0,
            "saved": 0,
            "errors": 0
        }
        
        try:
            # Step 1: Fetch recent articles
            articles = self.fetch_recent_articles()
            stats["fetched"] = len(articles)
            
            logger.info(f"Processing {len(articles)} articles...")
            
            # Step 2 & 3: Check duplicates and analyze new articles
            for article in articles:
                url = article.get('url')
                headline = article.get('headline', '')
                
                if not url:
                    continue
                
                try:
                    # Check if duplicate
                    if self.check_duplicate(url):
                        logger.info(f"Skipping duplicate article: {url}")
                        continue
                    
                    stats["new_articles"] += 1
                    
                    # Analyze article
                    analysis = self.analyze_article(url, headline)
                    
                    if analysis:
                        stats["analyzed"] += 1
                        
                        # Set URL from fetched article
                        analysis['url'] = url
                        if not analysis.get('headline'):
                            analysis['headline'] = headline
                        
                        # Save to Firestore
                        if self.save_to_firestore(analysis):
                            stats["saved"] += 1
                    else:
                        stats["errors"] += 1
                        logger.error(f"Failed to analyze article: {url}")
                        
                except Exception as e:
                    stats["errors"] += 1
                    logger.error(f"Error processing article {url}: {str(e)}")
                    continue
            
            logger.info(f"Pipeline complete. Stats: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Fatal error in pipeline: {str(e)}")
            stats["errors"] += 1
            return stats


def news_pipeline(request):
    """
    Cloud Function entry point
    Triggered by Cloud Scheduler every 15 minutes
    """
    logger.info("Starting news pipeline...")
    
    pipeline = NewsPipeline()
    stats = pipeline.run()
    
    logger.info(f"News pipeline completed successfully: {stats}")
    
    return {
        'statusCode': 200,
        'body': json.dumps(stats)
    }


# For local testing
if __name__ == "__main__":
    pipeline = NewsPipeline()
    stats = pipeline.run()
    print(f"Results: {stats}")
