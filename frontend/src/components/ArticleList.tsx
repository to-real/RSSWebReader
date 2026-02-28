import { useQuery } from '@tanstack/react-query'
import { articlesApi } from '../lib/api'
import { ArticleCard } from './ArticleCard'
import { useState } from 'react'

interface ArticleListProps {
  feedId?: number | null
  keyword?: string
}

export function ArticleList({ feedId, keyword }: ArticleListProps) {
  const [page, setPage] = useState(1)

  const { data, isLoading, error } = useQuery({
    queryKey: ['articles', page, feedId, keyword],
    queryFn: () => articlesApi.list({
      page,
      page_size: 20,
      feed_id: feedId || undefined,
      keyword: keyword || undefined,
    }).then(res => res.data),
  })

  if (isLoading) {
    return (
      <div className="p-8">
        {/* Loading skeleton */}
        {[1, 2, 3].map(i => (
          <div key={i} className="mb-4 p-5 rounded-xl" style={{ background: 'var(--bg-secondary)' }}>
            <div className="skeleton h-5 w-3/4 mb-3" />
            <div className="skeleton h-4 w-full mb-2" />
            <div className="skeleton h-4 w-2/3" />
          </div>
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-8 text-center">
        <div className="inline-flex items-center gap-3 px-4 py-3 rounded-xl" style={{ background: 'linear-gradient(135deg, #fee2e2 0%, #fecaca 100%)' }}>
          <svg className="w-5 h-5" style={{ color: '#991b1b' }} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span style={{ color: '#991b1b' }}>加载失败，请稍后重试</span>
        </div>
      </div>
    )
  }

  if (!data || data.items.length === 0) {
    return (
      <div className="p-8 text-center">
        <div className="py-12">
          <div className="w-16 h-16 mx-auto mb-4 rounded-2xl flex items-center justify-center" style={{ background: 'var(--bg-tertiary)' }}>
            <svg className="w-8 h-8" style={{ color: 'var(--fg-tertiary)' }} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
            </svg>
          </div>
          <p className="text-sm" style={{ color: 'var(--fg-secondary)' }}>
            {keyword ? '没有找到匹配的文章' : '文章正在采集中，预计几分钟后刷新即可看到内容'}
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="py-4">
      {/* Stats bar */}
      <div className="px-4 sm:px-6 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium" style={{ color: 'var(--fg-secondary)' }}>
            共 {data.total} 篇文章
          </span>
          {keyword && (
            <span className="tag" style={{ background: 'var(--accent-soft)', color: 'var(--accent)' }}>
              搜索: {keyword}
            </span>
          )}
        </div>
        <div className="text-xs" style={{ color: 'var(--fg-tertiary)' }}>
          第 {page} 页
        </div>
      </div>

      {/* Articles */}
      <div className="px-4 sm:px-6 space-y-4 stagger-children">
        {data.items.map(article => (
          <ArticleCard key={article.id} article={article} />
        ))}
      </div>

      {/* Pagination */}
      <div className="flex justify-center items-center gap-4 py-8">
        <button
          onClick={() => setPage(p => Math.max(1, p - 1))}
          disabled={page === 1}
          className="btn-ghost flex items-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
          上一页
        </button>

        <div className="flex items-center gap-1.5">
          {page > 2 && (
            <button
              onClick={() => setPage(1)}
              className="w-8 h-8 rounded-lg text-sm transition-colors"
              style={{ color: 'var(--fg-tertiary)' }}
            >
              1
            </button>
          )}
          {page > 2 && <span style={{ color: 'var(--fg-tertiary)' }}>...</span>}
          <button
            className="w-8 h-8 rounded-lg text-sm font-medium"
            style={{ background: 'var(--accent)', color: 'white' }}
          >
            {page}
          </button>
        </div>

        <button
          onClick={() => setPage(p => (data.has_next ? p + 1 : p))}
          disabled={!data.has_next}
          className="btn-ghost flex items-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed"
        >
          下一页
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
    </div>
  )
}
