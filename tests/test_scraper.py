import pytest
from web_scraper.scraper import BasicScraper

def test_scraper_initialization():
  scraper = BasicScraper()
  assert scraper is not None