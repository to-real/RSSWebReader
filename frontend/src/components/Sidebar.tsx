import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { feedsApi } from '../lib/api'
import { cn } from '../lib/utils'

interface SidebarProps {
  selectedCategory: string | null
  onSelectCategory: (category: string | null) => void
}

export function Sidebar({ selectedCategory, onSelectCategory }: SidebarProps) {
  const [isOpen, setIsOpen] = useState(false)
  const { data: categories } = useQuery({
    queryKey: ['categories'],
    queryFn: () => feedsApi.getCategories().then(res => res.data),
  })

  return (
    <>
      {/* Mobile toggle button */}
      <button
        className="md:hidden fixed bottom-4 right-4 z-50 bg-blue-500 text-white p-3 rounded-full shadow-lg"
        onClick={() => setIsOpen(!isOpen)}
      >
        {isOpen ? '×' : '☰'}
      </button>

      {/* Sidebar - desktop: always visible, mobile: drawer */}
      <aside className={cn(
        "fixed md:static inset-y-0 left-0 z-40 w-64 bg-gray-50 transform transition-transform duration-300",
        "md:min-h-screen md:transform-none md:transition-none",
        isOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
      )}>
        <div className="p-4">
          <h2 className="font-bold text-lg mb-4">分类</h2>

          <button
            onClick={() => { onSelectCategory(null); setIsOpen(false) }}
            className={cn(
              "w-full text-left px-3 py-2 rounded mb-1",
              !selectedCategory ? "bg-blue-100 text-blue-700" : "hover:bg-gray-100"
            )}
          >
            全部 Feeds
          </button>

          {categories?.map(cat => (
            <button
              key={cat}
              onClick={() => { onSelectCategory(cat); setIsOpen(false) }}
              className={cn(
                "w-full text-left px-3 py-2 rounded mb-1",
                selectedCategory === cat ? "bg-blue-100 text-blue-700" : "hover:bg-gray-100"
              )}
            >
              {cat}
            </button>
          ))}
        </div>
      </aside>

      {/* Overlay for mobile */}
      {isOpen && (
        <div
          className="md:hidden fixed inset-0 bg-black bg-opacity-50 z-30"
          onClick={() => setIsOpen(false)}
        />
      )}
    </>
  )
}
