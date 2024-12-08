# scraper.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict
import logging
from models import Article, WebsiteConfig, ScrapingResult, Settings
import hashlib
from config import WEBSITE_CONFIGS


class NewsScraperAgent:
    def __init__(self):
        self.settings = Settings()
        self.websites_config = [
            WebsiteConfig(**config) for config in WEBSITE_CONFIGS.values()
        ]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.logger = logging.getLogger(__name__)

    def generate_article_id(self, url: str, title: str) -> str:
        """Generate a unique ID for an article based on its URL and title."""
        content = f"{url}{title}".encode("utf-8")
        return hashlib.md5(content).hexdigest()

    async def scrape_website(self, config: WebsiteConfig) -> ScrapingResult:
        """Scrape articles from a single website."""
        try:
            response = requests.get(config.url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            articles = []
            for article_element in soup.select(config.article_selector):
                try:
                    title = article_element.select_one(
                        config.title_selector
                    ).text.strip()
                    content = article_element.select_one(
                        config.content_selector
                    ).text.strip()
                    date_text = article_element.select_one(
                        config.date_selector
                    ).text.strip()
                    published_date = datetime.strptime(date_text, config.date_format)
                    url = article_element.find("a")["href"]

                    article = Article(
                        id=self.generate_article_id(url, title),
                        title=title,
                        url=url,
                        source=config.name,
                        published_date=published_date,
                        summary="",  # Will be filled by the AI processor
                        content=content,
                    )
                    articles.append(article)
                except Exception as e:
                    self.logger.error(
                        f"Error processing article from {config.name}: {str(e)}"
                    )

            return ScrapingResult(success=True, articles=articles)

        except Exception as e:
            self.logger.error(f"Error scraping {config.name}: {str(e)}")
            return ScrapingResult(success=False, errors=[str(e)])

    async def scrape_all_websites(self) -> List[ScrapingResult]:
        """Scrape articles from all configured websites."""
        results = []
        for config in self.websites_config:
            result = await self.scrape_website(config)
            results.append(result)
        return results
