"""
Fixed taxonomy for public-facing source classification.
Standardized English categories used across backend, scripts, and frontend.
"""

# Domain categories - English (used in database, API, and frontend)
DOMAIN_CATEGORIES = [
    "AI/ML",
    "Engineering",
    "Business",
    "Security",
    "Web",
    "Systems",
    "Culture",
    "Science",
    "Design",
    "Productivity",
]

# Chinese labels for display purposes
DOMAIN_CATEGORY_LABELS = {
    "AI/ML": "AI/机器学习",
    "Engineering": "工程",
    "Business": "商业",
    "Security": "安全",
    "Web": "Web开发",
    "Systems": "系统",
    "Culture": "文化",
    "Science": "科学",
    "Design": "设计",
    "Productivity": "效率工具",
}

SOURCE_TYPES = [
    "Personal Blog",
    "Company Tech Blog",
    "Media",
    "Research Institution",
    "Community Organization",
]

SOURCE_TYPE_LABELS = {
    "Personal Blog": "个人博客",
    "Company Tech Blog": "公司技术博客",
    "Media": "媒体",
    "Research Institution": "研究机构",
    "Community Organization": "社区组织",
}

DOMAIN_CATEGORY_SET = set(DOMAIN_CATEGORIES)
SOURCE_TYPE_SET = set(SOURCE_TYPES)
