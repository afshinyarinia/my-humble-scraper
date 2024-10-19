import asyncio
import sys
import logging
from web_scraper.scraper import AdvancedScraper
from web_scraper.utils import read_urls_from_file
from web_scraper.scheduler import ScraperScheduler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def main():
  if len(sys.argv) < 2:
      print("Usage: poetry run scrape <url1> [url2 ...] OR poetry run scrape --file <urls_file> [--schedule <interval_minutes>]")
      sys.exit(1)

  scraper = AdvancedScraper()
  urls = []
  schedule_interval = None

  if sys.argv[1] == '--file':
      if len(sys.argv) < 3:
          print("Please provide a file path when using --file option.")
          sys.exit(1)
      urls = read_urls_from_file(sys.argv[2])
      if len(sys.argv) > 3 and sys.argv[3] == '--schedule':
          if len(sys.argv) < 5:
              print("Please provide an interval in minutes when using --schedule option.")
              sys.exit(1)
          schedule_interval = int(sys.argv[4])
  else:
      urls = sys.argv[1:]

  selectors = {
      'title': 'h1',
      'paragraphs': 'p',
      'links': 'a'
  }

  if schedule_interval:
      scheduler = ScraperScheduler()
      scheduler.add_job(urls, schedule_interval, selectors)
      scheduler.start()
      print(f"Scraper scheduled to run every {schedule_interval} minutes. Press Ctrl+C to exit.")
      try:
          # This will keep the main thread alive
          while True:
              await asyncio.sleep(1)
      except KeyboardInterrupt:
          scheduler.shutdown()
  else:
      results = await scraper.scrape_multiple_urls(urls, selectors)
      for url, result in zip(urls, results):
          if result:
              print(f"Content scraped and saved for {url}")
          else:
              print(f"Scraping failed for {url}. Check the logs for more information.")

if __name__ == "__main__":
  asyncio.run(main())