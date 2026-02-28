import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { articlesApi } from '../lib/api'
import { Article } from '../types'
import { formatDistanceToNow } from 'date-fns'
import { zhCN } from 'date-fns/locale'

interface ArticleCardProps {
  article: Article
}

export function ArticleCard({ article }: ArticleCardProps) {
  const [expanded, setExpanded] = useState(false)

  const { data: detail, isLoading } = useQuery({
    queryKey: ['article', article.id],
    queryFn: () => articlesApi.get(article.id).then(res => res.data),
    enabled: expanded,
  })

  const formatDate = (publishedAt: string | null, createdAt: string) => {
    // Use published_at if available, otherwise fall back to created_at
    const dateStr = publishedAt || createdAt
    if (!dateStr) return '未知时间'
    return formatDistanceToNow(new Date(dateStr), { addSuffix: true, locale: zhCN })
  }

  return (
    <article className="article-card animate-fade-in">
      {/* Title */}
      <a
        href={article.url}
        target="_blank"
        rel="noopener noreferrer"
        className="block group"
      >
        <h3
          className="text-lg font-semibold leading-snug transition-colors duration-200 font-serif"
          style={{ color: 'var(--fg-primary)' }}
        >
          <span className="group-hover:text-[var(--accent)] transition-colors duration-200">
            {article.title}
          </span>
        </h3>
      </a>

      {/* One-liner */}
      {article.one_liner && (
        <p
          className="mt-2 text-sm leading-relaxed"
          style={{ color: 'var(--fg-secondary)' }}
        >
          {article.one_liner}
        </p>
      )}

      {/* Keywords */}
      {article.keywords.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mt-3">
          {article.keywords.slice(0, 5).map(kw => (
            <span key={kw} className="tag">
              {kw}
            </span>
          ))}
        </div>
      )}

      {/* Expand button */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="mt-3 text-sm font-medium flex items-center gap-1.5 transition-colors duration-200"
        style={{ color: 'var(--accent)' }}
      >
        <svg
          className={`w-4 h-4 transition-transform duration-200 ${expanded ? 'rotate-180' : ''}`}
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={2}
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
        </svg>
        {expanded ? '收起摘要' : '展开摘要'}
      </button>

      {/* Expanded summary */}
      {expanded && (
        <div className="mt-4 animate-fade-in">
          {isLoading && (
            <div className="flex items-center gap-3 p-4 rounded-xl" style={{ background: 'var(--bg-tertiary)' }}>
              <div className="w-5 h-5 border-2 border-[var(--accent)] border-t-transparent rounded-full animate-spin" />
              <span className="text-sm" style={{ color: 'var(--fg-secondary)' }}>
                AI 正在生成摘要...
              </span>
            </div>
          )}
          {detail && detail.summary_status === 'pending' && (
            <div className="flex items-center gap-3 p-4 rounded-xl" style={{ background: 'linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)' }}>
              <span className="text-lg">⏳</span>
              <span className="text-sm" style={{ color: '#92400e' }}>
                AI 摘要生成中，通常需要几分钟
              </span>
            </div>
          )}
          {detail && detail.summary_status === 'failed' && (
            <div className="flex items-center gap-3 p-4 rounded-xl" style={{ background: 'linear-gradient(135deg, #fee2e2 0%, #fecaca 100%)' }}>
              <span className="text-lg">⚠️</span>
              <span className="text-sm" style={{ color: '#991b1b' }}>
                摘要生成失败，稍后会自动重试
              </span>
            </div>
          )}
          {detail && detail.summary_status === 'completed' && detail.summary_cn && (
            <div className="summary-box">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-base">💡</span>
                <span className="text-sm font-semibold" style={{ color: 'var(--fg-primary)' }}>
                  AI 摘要
                </span>
              </div>
              <p className="text-sm leading-relaxed" style={{ color: 'var(--fg-primary)' }}>
                {detail.summary_cn}
              </p>
              {detail.one_liner && (
                <p className="mt-2 text-sm italic" style={{ color: 'var(--fg-secondary)' }}>
                  「{detail.one_liner}」
                </p>
              )}
            </div>
          )}
          {detail?.source_type && (
            <div className="mt-3 flex items-center gap-2 text-xs" style={{ color: 'var(--fg-tertiary)' }}>
              <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              <span>{detail.source_type}</span>
            </div>
          )}
        </div>
      )}

      {/* Meta */}
      <div className="flex items-center gap-3 mt-4 pt-3 border-t" style={{ borderColor: 'var(--border-subtle)' }}>
        <div className="flex items-center gap-1.5 text-xs" style={{ color: 'var(--fg-tertiary)' }}>
          <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <span>{formatDate(article.published_at, article.created_at)}</span>
        </div>
        {article.feed_title && (
          <div className="flex items-center gap-1.5 text-xs" style={{ color: 'var(--fg-tertiary)' }}>
            <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 5c7.18 0 13 5.82 13 13M6 11a7 7 0 017 7m-6 0a1 1 0 11-2 0 1 1 0 012 0z" />
            </svg>
            <span>{article.feed_title}</span>
          </div>
        )}
      </div>
    </article>
  )
}
