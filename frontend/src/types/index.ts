export interface Article {
  id: number
  title: string
  url: string
  one_liner: string | null
  keywords: string[]
  published_at: string | null
  feed_title: string
  feed_category: string | null
}

export interface ArticleDetail extends Article {
  content: string
  content_hash: string
  author: string | null
  language: string
  summary_cn: string | null
  summary_status: 'pending' | 'completed' | 'failed'
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  has_next: boolean
}

export interface Feed {
  id: number
  url: string
  title: string
  description: string | null
  category: string | null
  is_active: boolean
  fetch_interval_minutes: number
  last_fetched_at: string | null
}

export interface Stats {
  total_feeds: number
  active_feeds: number
  total_articles: number
  articles_today: number
  summaries_pending: number
  summaries_failed: number
  summaries_completed: number
  last_fetch_at: string | null
  completion_rate: number
}
