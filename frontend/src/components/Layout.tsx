import { ReactNode, useState, useEffect } from 'react'
import { useDebounce } from '../hooks/useDebounce'

interface LayoutProps {
  children: ReactNode
  onSearch: (keyword: string) => void
}

export function Layout({ children, onSearch }: LayoutProps) {
  const [searchInput, setSearchInput] = useState('')
  const [darkMode, setDarkMode] = useState(() => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('darkMode') === 'true' ||
        window.matchMedia('(prefers-color-scheme: dark)').matches
    }
    return false
  })
  const debouncedSearch = useDebounce(searchInput, 300)

  useEffect(() => {
    onSearch(debouncedSearch)
  }, [debouncedSearch, onSearch])

  useEffect(() => {
    document.documentElement.classList.toggle('dark', darkMode)
    localStorage.setItem('darkMode', String(darkMode))
  }, [darkMode])

  return (
    <div className="min-h-screen transition-colors duration-300">
      {/* Header */}
      <header className="sticky top-0 z-50 glass border-b border-[var(--border-subtle)]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-[var(--accent)] to-violet-500 flex items-center justify-center shadow-lg">
                <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <div>
                <h1 className="text-lg font-semibold tracking-tight" style={{ color: 'var(--fg-primary)' }}>
                  RSS Reader
                </h1>
                <p className="text-xs" style={{ color: 'var(--fg-tertiary)' }}>智能摘要 · 技术资讯</p>
              </div>
            </div>

            {/* Search */}
            <div className="flex-1 max-w-md mx-8">
              <div className="relative">
                <svg
                  className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 pointer-events-none"
                  style={{ color: 'var(--fg-tertiary)' }}
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={2}
                >
                  <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <input
                  type="text"
                  placeholder="搜索文章标题或关键词..."
                  value={searchInput}
                  onChange={e => setSearchInput(e.target.value)}
                  onFocus={(e) => e.target.style.boxShadow = 'inset 0 0 0 1.5px var(--accent)'}
                  onBlur={(e) => e.target.style.boxShadow = 'inset 0 0 0 1px var(--border)'}
                  className="w-full py-2.5 pl-10 pr-10 text-sm rounded-xl border-none outline-none transition-shadow placeholder:text-[var(--fg-tertiary)]"
                  style={{
                    background: 'var(--bg-secondary)',
                    color: 'var(--fg-primary)',
                    boxShadow: 'inset 0 0 0 1px var(--border)',
                  }}
                />
                {searchInput && (
                  <button
                    onClick={() => setSearchInput('')}
                    className="absolute right-2 top-1/2 -translate-y-1/2 p-1.5 rounded-lg transition-colors"
                    style={{ color: 'var(--fg-tertiary)' }}
                    onMouseEnter={(e) => e.currentTarget.style.background = 'var(--bg-tertiary)'}
                    onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
                  >
                    <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                )}
              </div>
            </div>

            {/* Actions */}
            <div className="flex items-center gap-2">
              {/* Dark mode toggle */}
              <button
                onClick={() => setDarkMode(!darkMode)}
                className="btn-ghost p-2.5 rounded-lg"
                title={darkMode ? '切换到浅色模式' : '切换到深色模式'}
              >
                {darkMode ? (
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                  </svg>
                ) : (
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                  </svg>
                )}
              </button>

              {/* Refresh button */}
              <button
                className="btn-ghost p-2.5 rounded-lg"
                title="刷新"
                onClick={() => window.location.reload()}
              >
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto">
        {children}
      </main>

      {/* Footer */}
      <footer className="py-6 text-center text-sm" style={{ color: 'var(--fg-tertiary)' }}>
        <p>Powered by AI Summarization · Built with ❤️</p>
      </footer>
    </div>
  )
}
