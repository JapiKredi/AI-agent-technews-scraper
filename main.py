# main.py
import asyncio
import streamlit as st
from scraper import NewsScraperAgent
from datetime import datetime, timedelta
import pandas as pd
from config import WEBSITE_CONFIGS
import groq
from models import Settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize settings
settings = Settings()

# Initialize Groq client
client = groq.Groq(api_key=settings.groq_api_key)


async def summarize_article(content: str) -> str:
    """Summarize article content using Groq."""
    try:
        prompt = f"""Please provide a concise summary of the following article, focusing on the key points and insights:

        {content}

        Summary:"""

        completion = await client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="mixtral-8x7b-32768",
            temperature=0.3,
            max_tokens=500,
        )

        return completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Error summarizing article: {str(e)}")
        return "Error generating summary"


def initialize_session_state():
    """Initialize session state variables."""
    if "articles" not in st.session_state:
        st.session_state.articles = []
    if "last_update" not in st.session_state:
        st.session_state.last_update = None


async def fetch_and_process_articles():
    """Fetch and process articles from all sources."""
    scraper = NewsScraperAgent()
    results = await scraper.scrape_all_websites()

    all_articles = []
    for result in results:
        if result.success:
            for article in result.articles:
                # Summarize article content
                article.summary = await summarize_article(article.content)
                all_articles.append(article)

    return all_articles


def main():
    st.title("AI News Aggregator")

    # Initialize session state
    initialize_session_state()

    # Sidebar
    st.sidebar.title("Controls")
    if st.sidebar.button("Refresh Articles"):
        st.session_state.articles = asyncio.run(fetch_and_process_articles())
        st.session_state.last_update = datetime.now()

    # Filter options
    sources = list(WEBSITE_CONFIGS.keys())
    selected_sources = st.sidebar.multiselect(
        "Select Sources", sources, default=sources
    )

    days_ago = st.sidebar.slider("Show articles from last X days", 1, 30, 7)

    search_query = st.sidebar.text_input("Search articles")

    # Display last update time
    if st.session_state.last_update:
        st.sidebar.text(
            f"Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M')}"
        )

    # Filter and display articles
    if st.session_state.articles:
        filtered_articles = [
            article
            for article in st.session_state.articles
            if article.source in selected_sources
            and article.published_date >= datetime.now() - timedelta(days=days_ago)
        ]

        if search_query:
            filtered_articles = [
                article
                for article in filtered_articles
                if search_query.lower() in article.title.lower()
                or search_query.lower() in article.summary.lower()
            ]

        # Display articles
        for article in filtered_articles:
            with st.expander(f"{article.title} - {article.source}"):
                st.write(f"Published: {article.published_date.strftime('%Y-%m-%d')}")
                st.write("Summary:")
                st.write(article.summary)
                st.write("Original Article:")
                st.write(article.url)
    else:
        st.info("Click 'Refresh Articles' to fetch the latest news.")


if __name__ == "__main__":
    main()
