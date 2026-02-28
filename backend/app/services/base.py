"""
Base class for AI summarization services.
Provides common prompt building and response parsing utilities.
"""
import json
from abc import ABC, abstractmethod
from app.core.config import get_settings

settings = get_settings()


class BaseAIService(ABC):
    """Base class for AI summarization services"""

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
        """Parse AI response with defensive handling"""
        text = response_text.strip()
        # Remove markdown code blocks
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse AI response as JSON: {text[:200]}...") from e

    @abstractmethod
    async def summarize(self, title: str, content: str) -> dict:
        """Generate summary for article - must be implemented by subclasses"""
        pass
