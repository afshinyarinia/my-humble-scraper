import pytest
from web_scraper.scraper import AdvancedScraper

def test_scraper_initialization():
  scraper = AdvancedScraper()
  assert scraper is not None