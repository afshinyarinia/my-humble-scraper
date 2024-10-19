import sys
import logging
from web_scraper.scraper import BasicScraper

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
  if len(sys.argv) != 2:
      print("Usage: poetry run scrape <url>")
      sys.exit(1)

  url = sys.argv[1]
  scraper = BasicScraper()
  result = scraper.scrape_url(url)

  if result:
      print(f"Content scraped and saved to database")
  else:
      print("Scraping failed. Check the logs for more information.")

if __name__ == "__main__":
  main()
