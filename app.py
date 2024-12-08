# app.py
import streamlit as st
import asyncio
from datetime import datetime, timedelta
from typing import List
import json
import os

from models import Article, SearchQuery, WebsiteConfig
from scraper import NewsScraperAgent
from ai_processor import AIProcessor


# Load configuration
def load_website_configs() -> List[WebsiteConfig]:
    with open("config/websites.json", "r") as f:
        configs = json.load(f)
    return [WebsiteConfig(**config) for config in configs]


# Initialize components
websites_config = load_website_configs()
scraper = NewsScraperAgent(websites_config)
ai_processor = AIProcessor(api_key=os.getenv("GROQ_API_KEY"))

# Streamlit interface
st.title("AI Agent News Aggregator")

# Sidebar for filters
st.sidebar.header("Search Filters")
search_query = st.sidebar.text_input("Search Keywords")
date_range = st.sidebar.date_input(
    "Date Range", value=(datetime.now() - timedelta(days=7), datetime.now())
)
selected_sources = st.sidebar.multiselect(
    "Select Sources", options=[config.name for config in websites_config]
)

# Main content area
if st.button("Fetch Latest News"):
    with st.spinner("Fetching and processing articles..."):
        # Create search query
        query = SearchQuery(
            query=search_query,
            date_from=datetime.combine(date_range[0], datetime.min.time()),
            date_to=datetime.combine(date_range[1], datetime.max.time()),
            sources=selected_sources if selected_sources else None,
        )

        # Fetch and process articles
        async def fetch_and_process():
            # Scrape articles
            results = await scraper.scrape_all_websites()
            all_articles = []
            for result in results:
                if result.success:
                    all_articles.extend(result.articles)

            # Process articles with AI
            processed_articles = await ai_processor.process_articles(all_articles)
            return processed_articles

        # Run async operations
        articles = asyncio.run(fetch_and_process())

        # Filter articles based on search criteria
        filtered_articles = []
        for article in articles:
            matches_query = (
                not search_query
                or search_query.lower() in article.title.lower()
                or search_query.lower() in article.summary.lower()
            )
            matches_date = query.date_from <= article.published_date <= query.date_to
            matches_source = not selected_sources or article.source in selected_sources

            if matches_query and matches_date and matches_source:
                filtered_articles.append(article)

        # Display articles
        for article in filtered_articles:
            st.markdown(f"## {article.title}")
            st.markdown(f"**Source:** {article.source}")
            st.markdown(
                f"**Published:** {article.published_date.strftime('%Y-%m-%d %H:%M')}"
            )
            st.markdown("### Summary")
            st.write(article.summary)
            st.markdown("### Keywords")
            st.write(", ".join(article.keywords))
            st.markdown(f"[Read full article]({article.url})")
            st.markdown("---")

# Add a footer
st.markdown("---")
st.markdown("Powered by AI Agent News Aggregator")
