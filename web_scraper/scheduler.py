from apscheduler.schedulers.asyncio import AsyncIOScheduler
from web_scraper.scraper import AdvancedScraper

class ScraperScheduler:
  def __init__(self):
      self.scheduler = AsyncIOScheduler()
      self.scraper = AdvancedScraper()

  def add_job(self, urls, interval_minutes, selectors=None):
      self.scheduler.add_job(
          self.scraper.scrape_multiple_urls,
          'interval',
          minutes=interval_minutes,
          args=[urls, selectors]
      )

  def start(self):
      self.scheduler.start()

  def shutdown(self):
      self.scheduler.shutdown()