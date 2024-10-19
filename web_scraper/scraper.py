import requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import urlparse
from web_scraper.database import Database


class BasicScraper:
    def __init__(self):
        self.db = Database()

    def scrape_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.get_text()

            domain = urlparse(url).netloc

            self.db.save_data(url, domain, content)
            logging.info(f"Successfully scraped {url}")
            return content
        except requests.RequestException as e:
            logging.error(f"Error scraping {url}: {str(e)}")
            return None