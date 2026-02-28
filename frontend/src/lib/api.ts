import axios from 'axios'
import { PaginatedResponse, Article, ArticleDetail, Feed, Stats } from '../types'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
})

export const articlesApi = {
  list: (params: { page?: number; page_size?: number; feed_id?: number; category?: string; keyword?: string }) =>
    api.get<PaginatedResponse<Article>>('/articles/', { params }),

  getLatest: (limit = 20) =>
    api.get<Article[]>('/articles/latest', { params: { limit } }),

  get: (id: number) =>
    api.get<ArticleDetail>(`/articles/${id}`),
}

export const feedsApi = {
  list: () => api.get<Feed[]>('/feeds/'),

  getCategories: () => api.get<string[]>('/feeds/categories'),
}

export const statsApi = {
  get: () => api.get<Stats>('/stats'),
}

export const healthApi = {
  check: () => api.get<{ status: string }>('/health'),
}
