# config.py
import os
from dotenv import load_dotenv
from typing import Dict

# Load environment variables from .env file
load_dotenv()

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables")

# Website configurations
WEBSITE_CONFIGS = {
    "ai_magazine": {
        "name": "AI Magazine",
        "url": "https://aimagazine.com",
        "article_selector": "article.post",
        "title_selector": "h2.title",
        "content_selector": "div.content",
        "date_selector": "time.published",
        "date_format": "%Y-%m-%d",
    },
    "analytics_insight": {
        "name": "Analytics Insight",
        "url": "https://www.analyticsinsight.net",
        "article_selector": "div.td_module_10",
        "title_selector": "h3.entry-title",
        "content_selector": "div.td-post-content",
        "date_selector": "time.entry-date",
        "date_format": "%B %d, %Y",
    },
    "ai_trends": {
        "name": "AI Trends",
        "url": "https://www.aitrends.com",
        "article_selector": "article.post",
        "title_selector": "h2.entry-title",
        "content_selector": "div.entry-content",
        "date_selector": "time.entry-date",
        "date_format": "%Y-%m-%d",
    },
    "mit_news": {
        "name": "MIT News - AI",
        "url": "https://news.mit.edu/topic/artificial-intelligence2",
        "article_selector": "article.article-item",
        "title_selector": "h3.title",
        "content_selector": "div.article-content",
        "date_selector": "time.article-date",
        "date_format": "%B %d, %Y",
    },
    "wired": {
        "name": "Wired - AI",
        "url": "https://www.wired.com/tag/artificial-intelligence",
        "article_selector": "div.summary-item",
        "title_selector": "h3.summary-item__hed",
        "content_selector": "div.body__inner-container",
        "date_selector": "time.summary-item__timestamp",
        "date_format": "%Y-%m-%d",
    },
    "dataversity": {
        "name": "Dataversity",
        "url": "https://www.dataversity.net/category/artificial-intelligence",
        "article_selector": "article.post",
        "title_selector": "h2.entry-title",
        "content_selector": "div.entry-content",
        "date_selector": "time.entry-date",
        "date_format": "%B %d, %Y",
    },
    "openai": {
        "name": "OpenAI Blog",
        "url": "https://openai.com/blog",
        "article_selector": "article.post",
        "title_selector": "h2.post-title",
        "content_selector": "div.post-content",
        "date_selector": "time.post-date",
        "date_format": "%Y-%m-%d",
    },
    "ai_news": {
        "name": "AI News",
        "url": "https://artificialintelligence-news.com",
        "article_selector": "article.type-post",
        "title_selector": "h2.entry-title",
        "content_selector": "div.entry-content",
        "date_selector": "time.entry-date",
        "date_format": "%B %d, %Y",
    },
    "emerj": {
        "name": "Emerj",
        "url": "https://emerj.com/ai-sector-overviews",
        "article_selector": "article.post",
        "title_selector": "h2.entry-title",
        "content_selector": "div.entry-content",
        "date_selector": "time.entry-date",
        "date_format": "%B %d, %Y",
    },
    "extreme_tech": {
        "name": "ExtremeTech",
        "url": "https://www.extremetech.com/tag/artificial-intelligence",
        "article_selector": "article.article",
        "title_selector": "h2.title",
        "content_selector": "div.entry-content",
        "date_selector": "time.date",
        "date_format": "%Y-%m-%d",
    },
}

# Additional configuration settings
SCRAPING_SETTINGS = {
    "request_timeout": 30,  # seconds
    "max_retries": 3,
    "retry_delay": 5,  # seconds
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
}

# Cache settings
CACHE_SETTINGS = {
    "cache_duration": 3600,  # 1 hour in seconds
    "max_cache_items": 1000,
}

# Article processing settings
ARTICLE_SETTINGS = {
    "max_summary_length": 500,  # characters
    "min_article_length": 100,  # characters
    "max_keywords": 10,
}
