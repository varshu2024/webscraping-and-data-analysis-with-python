import requests
from bs4 import BeautifulSoup
from newspaper import Article
from urllib.parse import urljoin
import pandas as pd
from tqdm import tqdm
from datetime import datetime
import time
import random

class NewsScraper:
    def __init__(self, source_config):
        self.config = source_config
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def fetch_search_results(self, query, count=10, start=0):
        """Fetch search results for a query"""
        url = self.config['search_url'].format(
            query=query, count=count, start=start, page=1
        )
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.select(self.config['article_selector'])
            
            links = []
            for article in articles:
                href = article.get('href')
                if href and not href.startswith('http'):
                    href = urljoin(self.config['base_url'], href)
                links.append(href)
            
            return links
        
        except Exception as e:
            print(f"Error fetching search results: {e}")
            return []
    
    def scrape_article(self, url):
        """Scrape individual article content"""
        try:
            # Use newspaper3k for efficient article extraction
            article = Article(url)
            article.download()
            article.parse()
            
            # Additional metadata extraction if needed
            soup = BeautifulSoup(article.html, 'html.parser')
            
            date_element = soup.select_one(self.config['date_selector'])
            publish_date = None
            
            if date_element:
                try:
                    publish_date = datetime.strptime(date_element.text.strip(), self.config['date_format'])
                except ValueError:
                    publish_date = article.publish_date
            else:
                publish_date = article.publish_date
                
            return {
                'title': article.title,
                'text': article.text,
                'url': url,
                'date': publish_date,
                'authors': article.authors,
                'source': self.config['base_url']
            }
        
        except Exception as e:
            print(f"Error scraping article {url}: {e}")
            return None
    
    def scrape_articles(self, query, count=10, max_retries=3):
        """Scrape multiple articles for a query"""
        articles = []
        search_links = self.fetch_search_results(query, count)
        
        for link in tqdm(search_links, desc="Scraping articles"):
            retries = 0
            while retries < max_retries:
                try:
                    article_data = self.scrape_article(link)
                    if article_data:
                        articles.append(article_data)
                    break
                except Exception as e:
                    retries += 1
                    if retries == max_retries:
                        print(f"Failed to scrape {link} after {max_retries} attempts")
                    time.sleep(random.uniform(1, 3))
        
        return pd.DataFrame(articles)