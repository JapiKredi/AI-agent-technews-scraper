# ai_processor.py
from typing import List
import groq
from models import Article
import asyncio
import logging


class AIProcessor:
    def __init__(self, api_key: str):
        self.client = groq.Groq(api_key=api_key)
        self.logger = logging.getLogger(__name__)

    async def generate_summary(self, content: str) -> str:
        """Generate a summary of the article content using Claude."""
        try:
            prompt = f"""
            Please provide a concise summary of the following article. 
            Focus on the key points and main takeaways. Keep the summary under 200 words.

            Article:
            {content}
            """

            completion = await self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="mixtral-8x7b-32768",
                temperature=0.3,
                max_tokens=500,
            )

            return completion.choices[0].message.content

        except Exception as e:
            self.logger.error(f"Error generating summary: {str(e)}")
            return "Error generating summary"

    async def extract_keywords(self, content: str) -> List[str]:
        """Extract relevant keywords from the article content."""
        try:
            prompt = f"""
            Please extract 5-7 relevant keywords from the following article content.
            Return only the keywords as a comma-separated list.

            Article:
            {content}
            """

            completion = await self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="mixtral-8x7b-32768",
                temperature=0.3,
                max_tokens=100,
            )

            keywords = completion.choices[0].message.content.split(",")
            return [keyword.strip() for keyword in keywords]

        except Exception as e:
            self.logger.error(f"Error extracting keywords: {str(e)}")
            return []

    async def process_article(self, article: Article) -> Article:
        """Process a single article by generating summary and extracting keywords."""
        try:
            summary = await self.generate_summary(article.content)
            keywords = await self.extract_keywords(article.content)

            article.summary = summary
            article.keywords = keywords

            return article

        except Exception as e:
            self.logger.error(f"Error processing article: {str(e)}")
            return article

    async def process_articles(self, articles: List[Article]) -> List[Article]:
        """Process multiple articles concurrently."""
        tasks = [self.process_article(article) for article in articles]
        return await asyncio.gather(*tasks)
