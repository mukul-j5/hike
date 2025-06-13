import requests
import os
from datetime import datetime, timedelta
import streamlit as st
from typing import Dict, List, Optional

class DataFetcher:
    def __init__(self):
        self.cmc_api_key = "d073cbe0-a085-4d6f-8d8d-b3cf0ef9d7e3"
        self.news_api_key = os.getenv("NEWS_API_KEY", "")
        
        self.cmc_base_url = "https://pro-api.coinmarketcap.com/v1"
        self.news_base_url = "https://newsapi.org/v2"
        
        self.headers_cmc = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.cmc_api_key,
        }
    
    def get_market_data(self, symbols: List[str]) -> Dict:
        """Fetch market data for given cryptocurrency symbols from CoinMarketCap"""
        try:
            # Convert symbols to comma-separated string
            symbol_string = ','.join(symbols)
            
            url = f"{self.cmc_base_url}/cryptocurrency/quotes/latest"
            parameters = {
                'symbol': symbol_string,
                'convert': 'USD'
            }
            
            response = requests.get(url, headers=self.headers_cmc, params=parameters)
            
            if response.status_code == 200:
                data = response.json()
                market_data = {}
                
                if 'data' in data:
                    for symbol, info in data['data'].items():
                        quote = info['quote']['USD']
                        market_data[symbol] = {
                            'name': info['name'],
                            'symbol': info['symbol'],
                            'price': quote['price'],
                            'market_cap': quote['market_cap'] or 0,
                            'volume_24h': quote['volume_24h'] or 0,
                            'percent_change_1h': quote['percent_change_1h'] or 0,
                            'percent_change_24h': quote['percent_change_24h'] or 0,
                            'percent_change_7d': quote['percent_change_7d'] or 0,
                            'circulating_supply': info['circulating_supply'] or 0,
                            'total_supply': info['total_supply'] or 0,
                            'max_supply': info['max_supply'],
                            'last_updated': quote['last_updated']
                        }
                
                return market_data
            else:
                st.error(f"CoinMarketCap API Error: {response.status_code}")
                return {}
                
        except requests.exceptions.RequestException as e:
            st.error(f"Network error fetching market data: {str(e)}")
            return {}
        except Exception as e:
            st.error(f"Error processing market data: {str(e)}")
            return {}
    
    def get_top_cryptocurrencies(self, limit: int = 100) -> List[Dict]:
        """Fetch top cryptocurrencies by market cap"""
        try:
            url = f"{self.cmc_base_url}/cryptocurrency/listings/latest"
            parameters = {
                'start': '1',
                'limit': str(limit),
                'convert': 'USD'
            }
            
            response = requests.get(url, headers=self.headers_cmc, params=parameters)
            
            if response.status_code == 200:
                data = response.json()
                cryptocurrencies = []
                
                for crypto in data['data']:
                    quote = crypto['quote']['USD']
                    cryptocurrencies.append({
                        'id': crypto['id'],
                        'name': crypto['name'],
                        'symbol': crypto['symbol'],
                        'price': quote['price'],
                        'market_cap': quote['market_cap'] or 0,
                        'volume_24h': quote['volume_24h'] or 0,
                        'percent_change_24h': quote['percent_change_24h'] or 0,
                        'circulating_supply': crypto['circulating_supply'] or 0,
                        'cmc_rank': crypto['cmc_rank']
                    })
                
                return cryptocurrencies
            else:
                st.error(f"CoinMarketCap API Error: {response.status_code}")
                return []
                
        except Exception as e:
            st.error(f"Error fetching top cryptocurrencies: {str(e)}")
            return []
    
    def get_web3_news(self) -> List[Dict]:
        """Fetch Web3 and blockchain related news"""
        try:
            # Try NewsAPI first if key is available
            if self.news_api_key:
                return self._get_newsapi_articles()
            else:
                # Fallback to other free news sources
                return self._get_alternative_news()
                
        except Exception as e:
            st.error(f"Error fetching news: {str(e)}")
            return []
    
    def _get_newsapi_articles(self) -> List[Dict]:
        """Fetch articles from NewsAPI"""
        try:
            url = f"{self.news_base_url}/everything"
            params = {
                'q': 'Web3 OR blockchain OR cryptocurrency OR DeFi OR NFT OR "decentralized finance"',
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': 20,
                'from': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
                'apiKey': self.news_api_key
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                articles = []
                
                for article in data.get('articles', []):
                    articles.append({
                        'title': article['title'],
                        'description': article['description'],
                        'url': article['url'],
                        'source': article['source']['name'],
                        'published_at': article['publishedAt']
                    })
                
                return articles
            else:
                return []
                
        except Exception as e:
            return []
    
    def _get_alternative_news(self) -> List[Dict]:
        """Fallback news source when NewsAPI is not available"""
        try:
            # Using CoinDesk RSS feed as alternative
            import feedparser
            
            feed_url = "https://www.coindesk.com/arc/outboundfeeds/rss/"
            feed = feedparser.parse(feed_url)
            
            articles = []
            for entry in feed.entries[:10]:
                articles.append({
                    'title': entry.title,
                    'description': entry.get('summary', ''),
                    'url': entry.link,
                    'source': 'CoinDesk',
                    'published_at': entry.get('published', '')
                })
            
            return articles
            
        except ImportError:
            # If feedparser is not available, return sample structure
            return [
                {
                    'title': 'Web3 News Feed Unavailable',
                    'description': 'Please configure NEWS_API_KEY environment variable for live news feed.',
                    'url': '#',
                    'source': 'System',
                    'published_at': datetime.now().isoformat()
                }
            ]
        except Exception:
            return []
    
    def get_project_metadata(self, symbols: List[str]) -> Dict:
        """Get additional metadata for projects"""
        try:
            url = f"{self.cmc_base_url}/cryptocurrency/info"
            parameters = {
                'symbol': ','.join(symbols)
            }
            
            response = requests.get(url, headers=self.headers_cmc, params=parameters)
            
            if response.status_code == 200:
                data = response.json()
                metadata = {}
                
                for symbol, info in data.get('data', {}).items():
                    metadata[symbol] = {
                        'description': info.get('description', ''),
                        'website': info.get('urls', {}).get('website', []),
                        'category': info.get('category', ''),
                        'tags': info.get('tags', []),
                        'platform': info.get('platform', {})
                    }
                
                return metadata
            else:
                return {}
                
        except Exception as e:
            return {}
