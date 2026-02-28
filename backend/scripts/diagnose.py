#!/usr/bin/env python
"""
Quick diagnostic script for RSS Web Reader
Run this after any code changes to verify system health.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from app.core.db import SessionLocal
from app.models import Feed, Article, Summary


def diagnose():
    db = SessionLocal()

    print("=" * 50)
    print(" RSS Web Reader 诊断报告")
    print("=" * 50)

    # Feeds
    feeds_total = db.query(Feed).count()
    feeds_active = db.query(Feed).filter(Feed.is_active == True).count()
    feeds_no_articles = db.query(Feed).filter(
        ~Feed.id.in_(db.query(Article.feed_id).distinct())
    ).count()

    # Articles
    articles_total = db.query(Article).count()
    articles_no_content = db.query(Article).filter(
        (Article.content == None) | (Article.content == "")
    ).count()

    # Summaries
    summary_stats = {}
    for status in ["pending", "completed", "failed"]:
        summary_stats[status] = db.query(Summary).filter(Summary.status == status).count()

    # Failed samples
    failed = db.query(Summary).filter(Summary.status == "failed").limit(5).all()

    # Categories
    categories = db.query(Feed.category).distinct().all()
    cats = [c[0] for c in categories if c[0]]

    print(f"\n【数据统计】")
    print(f"  Feeds: {feeds_active}/{feeds_total} 活跃, {feeds_no_articles} 个无文章")
    print(f"  Articles: {articles_total} 篇, {articles_no_content} 篇无正文")
    print(f"  Summaries: {summary_stats}")

    if cats:
        print(f"  Categories: {len(cats)} 个")
    else:
        print(f"  Categories: ❌ 无分类！")

    # Issues detection
    issues = []

    if feeds_no_articles > 10:
        issues.append(f"P1: {feeds_no_articles} 个 feeds 没有抓到文章")

    if articles_no_content > 100:
        issues.append(f"P1: {articles_no_content} 篇文章无正文内容")

    if summary_stats["failed"] > 0:
        issues.append(f"P0: {summary_stats['failed']} 篇摘要生成失败")

    if summary_stats["pending"] > 1000:
        issues.append(f"P1: {summary_stats['pending']} 篇待处理摘要")

    if not cats:
        issues.append("P2: feeds 没有分类标签")

    # Sample completed summary
    completed_sample = db.query(Summary).filter(
        Summary.status == "completed"
    ).first()

    if completed_sample:
        a = db.query(Article).filter(Article.id == completed_sample.article_id).first()
        print(f"\n【摘要样例】")
        print(f"  Article: {a.title if a else 'N/A'}")
        print(f"  One-liner: {completed_sample.one_liner[:50] if completed_sample.one_liner else 'None'}...")
    else:
        issues.append("P0: 没有已完成的摘要，AI 处理可能有问题")
        print(f"\n【摘要样例】❌ 无")

    # Failed samples
    if failed:
        print(f"\n【失败摘要样例】")
        for s in failed:
            print(f"  Article #{s.article_id}: {s.error[:80] if s.error else 'no error msg'}...")

    # Priority list
    if issues:
        print(f"\n【问题清单】")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
    else:
        print(f"\n【问题清单】✅ 未发现明显问题")

    print("=" * 50)
    db.close()


if __name__ == "__main__":
    diagnose()
