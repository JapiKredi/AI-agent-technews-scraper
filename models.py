# models.py
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable validation."""

    groq_api_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class Article(BaseModel):
    """Represents a news article with its metadata and content."""

    id: str = Field(..., description="Unique identifier for the article")
    title: str = Field(..., description="Title of the article")
    url: HttpUrl = Field(..., description="URL of the original article")
    source: str = Field(..., description="Source website of the article")
    published_date: datetime = Field(..., description="Publication date of the article")
    summary: str = Field(..., description="AI-generated summary of the article")
    keywords: List[str] = Field(
        default_factory=list, description="Keywords extracted from the article"
    )
    content: str = Field(..., description="Full content of the article")
    processed_date: datetime = Field(
        default_factory=datetime.now, description="Date when the article was processed"
    )


class SearchQuery(BaseModel):
    """Represents a user's search query."""

    query: str = Field(..., description="Search term or phrase")
    date_from: Optional[datetime] = Field(
        None, description="Start date for search range"
    )
    date_to: Optional[datetime] = Field(None, description="End date for search range")
    sources: Optional[List[str]] = Field(
        None, description="List of sources to search from"
    )


class WebsiteConfig(BaseModel):
    """Configuration for each news website to be scraped."""

    name: str = Field(..., description="Name of the website")
    url: HttpUrl = Field(..., description="Base URL of the website")
    article_selector: str = Field(..., description="CSS selector for article elements")
    title_selector: str = Field(..., description="CSS selector for article title")
    content_selector: str = Field(..., description="CSS selector for article content")
    date_selector: str = Field(..., description="CSS selector for article date")
    date_format: str = Field(..., description="Format string for parsing dates")


class ScrapingResult(BaseModel):
    """Results from a scraping operation."""

    success: bool = Field(..., description="Whether the scraping was successful")
    articles: List[Article] = Field(
        default_factory=list, description="List of scraped articles"
    )
    errors: List[str] = Field(
        default_factory=list, description="List of errors encountered during scraping"
    )
