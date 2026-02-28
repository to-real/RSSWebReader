import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { feedsApi } from '../lib/api'
import { cn } from '../lib/utils'

interface SidebarProps {
  selectedFeedId: number | null
  onSelectFeed: (feedId: number | null) => void
}

export function Sidebar({ selectedFeedId, onSelectFeed }: SidebarProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(new Set())

  const { data: feeds } = useQuery({
    queryKey: ['feeds'],
    queryFn: () => feedsApi.list().then(res => res.data),
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
  const sortedCategories = Object.keys(feedsByCategory || {}).sort(
    (a, b) => categoryOrder.indexOf(a) - categoryOrder.indexOf(b)
  )

  return (
    <>
      {/* Mobile toggle */}
      <button
        className="md:hidden fixed bottom-4 right-4 z-50 bg-blue-500 text-white p-3 rounded-full shadow-lg"
        onClick={() => setIsOpen(!isOpen)}
      >
        {isOpen ? '×' : '☰'}
      </button>

      {/* Sidebar */}
      <aside className={cn(
        "fixed md:static inset-y-0 left-0 z-40 w-64 bg-gray-50 transform transition-transform duration-300",
        "md:min-h-screen md:transform-none md:transition-none overflow-y-auto",
        isOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
      )}>
        <div className="p-4">
          <h2 className="font-bold text-lg mb-4">信源 ({feeds?.length || 0})</h2>

          {/* All articles button */}
          <button
            onClick={() => { onSelectFeed(null); setIsOpen(false) }}
            className={cn(
              "w-full text-left px-3 py-2 rounded mb-3 text-sm font-medium",
              !selectedFeedId ? "bg-blue-100 text-blue-700" : "hover:bg-gray-100"
            )}
          >
            📰 全部文章
          </button>

          {/* Categories */}
          <div className="space-y-1">
            {sortedCategories.map(cat => {
              const catFeeds = feedsByCategory?.[cat] || []
              const isExpanded = expandedCategories.has(cat)

              return (
                <div key={cat}>
                  {/* Category header */}
                  <button
                    onClick={() => toggleCategory(cat)}
                    className="w-full flex items-center justify-between px-3 py-1.5 text-xs font-semibold text-gray-500 uppercase tracking-wide hover:bg-gray-100 rounded"
                  >
                    <span>{cat} ({catFeeds.length})</span>
                    <span className={cn("transition-transform", isExpanded && "rotate-90")}>
                      ▸
                    </span>
                  </button>

                  {/* Feeds in category */}
                  {isExpanded && (
                    <div className="ml-2 border-l-2 border-gray-200 pl-2">
                      {catFeeds.map(feed => (
                        <button
                          key={feed.id}
                          onClick={() => { onSelectFeed(feed.id); setIsOpen(false) }}
                          className={cn(
                            "w-full text-left px-2 py-1 text-sm truncate rounded",
                            selectedFeedId === feed.id
                              ? "bg-blue-100 text-blue-700"
                              : "hover:bg-gray-100 text-gray-700"
                          )}
                          title={feed.title}
                        >
                          {feed.title}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </div>
      </aside>

      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="md:hidden fixed inset-0 bg-black bg-opacity-50 z-30"
          onClick={() => setIsOpen(false)}
        />
      )}
    </>
  )
}
