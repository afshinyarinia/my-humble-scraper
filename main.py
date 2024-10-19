# scraper.py

import requests
from bs4 import BeautifulSoup
import sqlite3
import logging
from urllib.parse import urlparse

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BasicScraper:
    def __init__(self, db_name='scraper.db'):
        self.db_name = db_name
        self.setup_database()

    def setup_database(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS scraped_data
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT,
                    domain TEXT,
                    content TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()

    def scrape_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.get_text()

            domain = urlparse(url).netloc

            self.save_to_database(url, domain, content)
            logging.info(f"Successfully scraped {url}")
            return content
        except requests.RequestException as e:
            logging.error(f"Error scraping {url}: {str(e)}")
            return None

    def save_to_database(self, url, domain, content):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("INSERT INTO scraped_data (url, domain, content) VALUES (?, ?, ?)",
                  (url, domain, content))
        conn.commit()
        conn.close()

# Command-line interface
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python scraper.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    scraper = BasicScraper()
    result = scraper.scrape_url(url)

    if result:
        print(f"Content scraped and saved to database: {scraper.db_name}")
    else:
        print("Scraping failed. Check the logs for more information.")

# Created/Modified files during execution:
print("scraper.db")