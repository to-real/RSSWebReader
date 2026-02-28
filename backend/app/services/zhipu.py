"""
Zhipu AI (BigModel) service for article summarization.
Supports GLM-4 and other models via Zhipu AI API.
"""
import json
from zhipuai import AsyncZhipuAI
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import get_settings
from app.core import logger

settings = get_settings()

class ZhipuService:
    """Zhipu AI service for generating Chinese summaries"""

    def __init__(self):
        api_key = getattr(settings, 'zhipu_api_key', None) or settings.claude_api_key
        if not api_key or api_key == "your-claude-api-key-here":
            raise ValueError("ZHIPU_API_KEY not configured in .env")

        self.client = AsyncZhipuAI(api_key=api_key)
        self.model = "glm-4-flash"  # Fast and cost-effective, or "glm-4" for higher quality

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
        """Parse Zhipu response with defensive handling"""
        text = response_text.strip()
        # Remove markdown code blocks
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        return json.loads(text)

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
