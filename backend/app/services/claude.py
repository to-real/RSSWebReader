import os
from anthropic import AsyncAnthropic
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import get_settings
from app.core import logger
from app.services.base import BaseAIService

settings = get_settings()


class ClaudeService(BaseAIService):
    """Claude/Zhipu AI service via Anthropic-compatible endpoint"""

    def __init__(self):
        # Support Zhipu via Anthropic-compatible endpoint
        api_key = settings.anthropic_api_key or os.getenv("ANTHROPIC_API_KEY") or settings.claude_api_key
        base_url = settings.anthropic_base_url or os.getenv("ANTHROPIC_BASE_URL")

        self.client = AsyncAnthropic(
            api_key=api_key,
            base_url=base_url  # None uses default, or set to Zhipu's endpoint
        )
        # Model name - Zhipu's Anthropic-compatible endpoint maps this internally
        self.model = "claude-3-5-sonnet-20241022"

    @retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5))
    async def summarize(self, title: str, content: str) -> dict:
        """Generate summary for article"""
        prompt = self._build_prompt(title, content)

        response = await self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        result = self._parse_response(response.content[0].text)
        logger.info("claude_summary_generated", title=title)
        return result
