import asyncio
import aiohttp
from bs4 import BeautifulSoup
import logging
from urllib.parse import urlparse
from web_scraper.database import Database
from web_scraper.utils import clean_data


class AdvancedScraper:
    def __init__(self):
        self.db = Database()

    async def scrape_url(self, url, session, selectors=None):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    soup = BeautifulSoup(content, 'html.parser')

                    if selectors:
                        extracted_data = {}
                        for key, selector in selectors.items():
                            elements = soup.select(selector)
                            extracted_data[key] = [elem.get_text(strip=True) for elem in elements]
                        content = str(extracted_data)
                    else:
                        content = soup.get_text()

                    domain = urlparse(url).netloc
                    cleaned_content = clean_data(content)

                    self.db.save_data(url, domain, cleaned_content)
                    logging.info(f"Successfully scraped {url}")
                    return cleaned_content
                else:
                    logging.error(f"Error scraping {url}: HTTP {response.status}")
                    return None
        except Exception as e:
            logging.error(f"Error scraping {url}: {str(e)}")
            return None

    async def scrape_multiple_urls(self, urls, selectors=None):
        async with aiohttp.ClientSession() as session:
            tasks = [self.scrape_url(url, session, selectors) for url in urls]
            return await asyncio.gather(*tasks)