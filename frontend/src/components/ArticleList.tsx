import { useQuery } from '@tanstack/react-query'
import { articlesApi } from '../lib/api'
import { ArticleCard } from './ArticleCard'
import { useState } from 'react'

interface ArticleListProps {
  category?: string | null
  keyword?: string
}

export function ArticleList({ category, keyword }: ArticleListProps) {
  const [page, setPage] = useState(1)

  const { data, isLoading, error } = useQuery({
    queryKey: ['articles', page, category, keyword],
    queryFn: () => articlesApi.list({
      page,
      page_size: 20,
      keyword: keyword || undefined,
    }).then(res => res.data),
  })

  if (isLoading) {
    return <div className="p-8 text-center text-gray-500">加载中...</div>
  }

  if (error) {
    return <div className="p-8 text-center text-red-500">加载失败，请稍后重试</div>
  }

  if (!data || data.items.length === 0) {
    return (
      <div className="p-8 text-center text-gray-500">
        {keyword ? '没有找到匹配的文章' : '文章正在采集中，预计几分钟后刷新即可看到内容'}
      </div>
    )
  }

  return (
    <div>
      <div className="px-4 py-2 text-sm text-gray-500">
        共 {data.total} 篇文章
      </div>

      {data.items.map(article => (
        <ArticleCard key={article.id} article={article} />
      ))}

      {/* Pagination */}
      <div className="flex justify-center gap-2 py-4">
        <button
          onClick={() => setPage(p => Math.max(1, p - 1))}
          disabled={page === 1}
          className="px-4 py-2 border rounded disabled:opacity-50"
        >
          上一页
        </button>
        <span className="px-4 py-2">第 {page} 页</span>
        <button
          onClick={() => setPage(p => (data.has_next ? p + 1 : p))}
          disabled={!data.has_next}
          className="px-4 py-2 border rounded disabled:opacity-50"
        >
          下一页
        </button>
      </div>
    </div>
  )
}
