"""
Zhipu AI (BigModel) service for article summarization.
Supports GLM-4 and other models via Zhipu AI API.
"""
from zhipuai import AsyncZhipuAI
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import get_settings
from app.core import logger
from app.services.base import BaseAIService

settings = get_settings()


class ZhipuService(BaseAIService):
    """Zhipu AI service for generating Chinese summaries"""

    def __init__(self):
        api_key = getattr(settings, 'zhipu_api_key', None) or settings.claude_api_key
        if not api_key or api_key == "your-claude-api-key-here":
            raise ValueError("ZHIPU_API_KEY not configured in .env")

        self.client = AsyncZhipuAI(api_key=api_key)
        self.model = "glm-4-flash"  # Fast and cost-effective, or "glm-4" for higher quality

    @retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5))
    async def summarize(self, title: str, content: str) -> dict:
        """Generate summary for article using Zhipu AI"""
        prompt = self._build_prompt(title, content)

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是一个专业的技术文章摘要助手，擅长将英文技术文章总结为简洁的中文摘要。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000,
        )

        result = self._parse_response(response.choices[0].message.content)
        logger.info("zhipu_summary_generated", title=title, model=self.model)
        return result
