"""
Fixed taxonomy for public-facing source classification.
"""

DOMAIN_CATEGORIES = [
    "AI",
    "安全",
    "系统",
    "前端",
    "后端",
    "数据",
    "产品",
    "商业",
    "设计",
    "科学",
]

SOURCE_TYPES = [
    "个人博客",
    "公司技术博客",
    "媒体",
    "研究机构",
    "社区组织",
]

DOMAIN_CATEGORY_SET = set(DOMAIN_CATEGORIES)
SOURCE_TYPE_SET = set(SOURCE_TYPES)
