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

  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return ''
    return formatDistanceToNow(new Date(dateStr), { addSuffix: true, locale: zhCN })
  }

  return (
    <article className="border-b border-gray-200 py-4">
      {/* Title */}
      <a
        href={article.url}
        target="_blank"
        rel="noopener noreferrer"
        className="text-lg font-semibold text-gray-900 hover:text-blue-600"
      >
        {article.title}
      </a>

      {/* One-liner */}
      {article.one_liner && (
        <p className="text-sm text-gray-600 mt-1">{article.one_liner}</p>
      )}

      {/* Keywords */}
      {article.keywords.length > 0 && (
        <div className="flex flex-wrap gap-2 mt-2">
          {article.keywords.map(kw => (
            <span key={kw} className="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">
              {kw}
            </span>
          ))}
        </div>
      )}

      {/* Expand button */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="text-sm text-blue-500 mt-2 hover:underline"
      >
        {expanded ? '收起' : '展开摘要'}
      </button>

      {/* Expanded summary */}
      {expanded && (
        <div className="mt-2">
          {isLoading && (
            <div className="bg-yellow-50 p-3 rounded text-sm text-yellow-700">
              ⏳ AI 正在生成摘要...
            </div>
          )}
          {detail && detail.summary_status === 'pending' && (
            <div className="bg-yellow-50 p-3 rounded text-sm text-yellow-700">
              ⏳ AI 摘要生成中，通常需要几分钟
            </div>
          )}
          {detail && detail.summary_status === 'failed' && (
            <div className="bg-red-50 p-3 rounded text-sm text-red-700">
              ⚠️ 摘要生成失败，稍后会自动重试
            </div>
          )}
          {detail && detail.summary_status === 'completed' && detail.summary_cn && (
            <div className="bg-gray-50 p-3 rounded text-sm">
              <p className="font-semibold mb-1">💡 一句话推荐</p>
              <p className="text-gray-600 mb-2">{detail.one_liner}</p>
              <p className="text-gray-700">{detail.summary_cn}</p>
            </div>
          )}
          {detail?.source_type && (
            <div className="mt-2 text-xs text-gray-500">
              Source type: {detail.source_type}
            </div>
          )}
        </div>
      )}

      {/* Meta */}
      <div className="text-xs text-gray-400 mt-2">
        {article.feed_title} · {formatDate(article.published_at)}
      </div>
    </article>
  )
}
