import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { feedsApi } from '../lib/api'

interface SidebarProps {
  selectedFeedId: number | null
  onSelectFeed: (feedId: number | null) => void
}

// Category icons for visual appeal
const categoryIcons: Record<string, string> = {
  'AI/ML': '🤖',
  'Engineering': '⚙️',
  'Business': '💼',
  'Security': '🔒',
  'Web': '🌐',
  'Systems': '🖥️',
  'Culture': '🎭',
  'Science': '🔬',
  'Design': '🎨',
  'Productivity': '📊',
  '未分类': '📁',
}

export function Sidebar({ selectedFeedId, onSelectFeed }: SidebarProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(new Set(['AI/ML']))

  const { data: feeds } = useQuery({
    queryKey: ['feeds'],
    queryFn: () => feedsApi.list().then(res => res.data),
    staleTime: 10 * 1000,
  })

  // Group feeds by category
  const feedsByCategory = feeds?.reduce((acc, feed) => {
    const cat = feed.category || '未分类'
    if (!acc[cat]) acc[cat] = []
    acc[cat].push(feed)
    return acc
  }, {} as Record<string, typeof feeds>)

  const toggleCategory = (cat: string) => {
    setExpandedCategories(prev => {
      const next = new Set(prev)
      if (next.has(cat)) {
        next.delete(cat)
      } else {
        next.add(cat)
      }
      return next
    })
  }

  // Category order (popular first)
  const categoryOrder = ['AI/ML', 'Engineering', 'Business', 'Security', 'Web', 'Systems', 'Culture', 'Science', 'Design', 'Productivity', '未分类']
  const sortedCategories = Object.keys(feedsByCategory || {}).sort((a, b) => {
    const aIdx = categoryOrder.indexOf(a)
    const bIdx = categoryOrder.indexOf(b)
    return (aIdx === -1 ? 999 : aIdx) - (bIdx === -1 ? 999 : bIdx)
  })

  return (
    <>
      {/* Mobile toggle */}
      <button
        className="md:hidden fixed bottom-6 right-6 z-50 w-12 h-12 rounded-full shadow-lg flex items-center justify-center transition-all duration-300 hover:scale-105"
        style={{
          background: 'linear-gradient(135deg, var(--accent) 0%, #8b5cf6 100%)',
          color: 'white',
        }}
        onClick={() => setIsOpen(!isOpen)}
      >
        {isOpen ? (
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        ) : (
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        )}
      </button>

      {/* Sidebar */}
      <aside
        className={`
          fixed md:sticky top-16 md:top-0 left-0 z-40 h-[calc(100vh-4rem)] md:h-[calc(100vh-0rem)]
          w-72 transition-transform duration-300 ease-out
          md:transform-none overflow-hidden
          ${isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
        `}
        style={{ background: 'var(--bg-secondary)', borderRight: '1px solid var(--border-subtle)' }}
      >
        <div className="h-full overflow-y-auto p-4">
          {/* Header */}
          <div className="mb-4 px-2">
            <h2 className="text-sm font-semibold uppercase tracking-wider" style={{ color: 'var(--fg-tertiary)' }}>
              订阅源
            </h2>
            <p className="text-xs mt-0.5" style={{ color: 'var(--fg-tertiary)' }}>
              {feeds?.length || 0} 个信源
            </p>
          </div>

          {/* All articles button */}
          <button
            onClick={() => { onSelectFeed(null); setIsOpen(false) }}
            className="w-full text-left px-3 py-2.5 rounded-xl mb-3 text-sm font-medium flex items-center gap-3 transition-all duration-200"
            style={{
              background: !selectedFeedId ? 'var(--accent-soft)' : 'transparent',
              color: !selectedFeedId ? 'var(--accent)' : 'var(--fg-secondary)',
            }}
          >
            <span
              className="w-8 h-8 rounded-lg flex items-center justify-center text-lg"
              style={{ background: !selectedFeedId ? 'var(--accent)' : 'var(--bg-tertiary)' }}
            >
              📰
            </span>
            <span>全部文章</span>
          </button>

          {/* Categories */}
          <div className="space-y-1 animate-fade-in">
            {sortedCategories.map(cat => {
              const catFeeds = feedsByCategory?.[cat] || []
              const isExpanded = expandedCategories.has(cat)

              return (
                <div key={cat}>
                  {/* Category header */}
                  <button
                    onClick={() => toggleCategory(cat)}
                    className="w-full flex items-center justify-between px-3 py-2 rounded-lg text-xs font-semibold uppercase tracking-wide transition-colors duration-200 hover:bg-[var(--bg-tertiary)]"
                    style={{ color: 'var(--fg-tertiary)' }}
                  >
                    <div className="flex items-center gap-2">
                      <span>{categoryIcons[cat] || '📁'}</span>
                      <span>{cat}</span>
                      <span
                        className="px-1.5 py-0.5 rounded-md text-[10px]"
                        style={{ background: 'var(--bg-tertiary)' }}
                      >
                        {catFeeds.length}
                      </span>
                    </div>
                    <svg
                      className={`w-4 h-4 transition-transform duration-200 ${isExpanded ? 'rotate-90' : ''}`}
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      strokeWidth={2}
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                    </svg>
                  </button>

                  {/* Feeds in category */}
                  <div
                    className={`overflow-hidden transition-all duration-300 ease-out ${isExpanded ? 'max-h-[1000px] opacity-100' : 'max-h-0 opacity-0'}`}
                  >
                    <div className="ml-4 border-l-2 pl-3 py-1 space-y-0.5" style={{ borderColor: 'var(--border)' }}>
                      {catFeeds.map(feed => (
                        <button
                          key={feed.id}
                          onClick={() => { onSelectFeed(feed.id); setIsOpen(false) }}
                          className="w-full text-left px-2.5 py-2 rounded-lg text-sm truncate transition-all duration-200 group"
                          style={{
                            background: selectedFeedId === feed.id ? 'var(--accent-soft)' : 'transparent',
                            color: selectedFeedId === feed.id ? 'var(--accent)' : 'var(--fg-secondary)',
                          }}
                          title={feed.title}
                        >
                          <span className="group-hover:translate-x-0.5 inline-block transition-transform duration-200">
                            {feed.title}
                          </span>
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </aside>

      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="md:hidden fixed inset-0 bg-black/30 backdrop-blur-sm z-30 animate-fade-in"
          onClick={() => setIsOpen(false)}
        />
      )}
    </>
  )
}
