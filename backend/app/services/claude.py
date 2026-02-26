import json
from anthropic import AsyncAnthropic
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import get_settings
from app.core import logger

settings = get_settings()

class ClaudeService:
    def __init__(self):
        self.client = AsyncAnthropic(api_key=settings.claude_api_key)
        self.model = "claude-3-5-sonnet-20241022"

    def _build_prompt(self, article_title: str, article_content: str) -> str:
        """Build prompt for article summarization"""
        truncated = article_content[:settings.claude_max_content_length]
        return f"""请阅读以下英文技术文章，生成中文摘要。

标题：{article_title}
正文：{truncated}

请严格按以下 JSON 格式返回，不要包含其他内容：
{{
  "summary": "200字以内的中文摘要",
  "one_liner": "一句话推荐理由，不超过30字",
  "keywords": ["关键词1", "关键词2", "关键词3"]
}}"""

    def _parse_response(self, response_text: str) -> dict:
        """Parse Claude response with defensive handling"""
        text = response_text.strip()
        # Remove markdown code blocks
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        return json.loads(text)

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
