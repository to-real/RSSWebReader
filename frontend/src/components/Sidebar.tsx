import { useQuery } from '@tanstack/react-query'
import { feedsApi } from '../lib/api'
import { cn } from '../lib/utils'

interface SidebarProps {
  selectedCategory: string | null
  onSelectCategory: (category: string | null) => void
}

export function Sidebar({ selectedCategory, onSelectCategory }: SidebarProps) {
  const { data: categories } = useQuery({
    queryKey: ['categories'],
    queryFn: () => feedsApi.getCategories().then(res => res.data),
  })

  return (
    <aside className="w-full md:w-64 bg-gray-50 md:min-h-screen p-4">
      <h2 className="font-bold text-lg mb-4">分类</h2>

      <button
        onClick={() => onSelectCategory(null)}
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
          onClick={() => onSelectCategory(cat)}
          className={cn(
            "w-full text-left px-3 py-2 rounded mb-1",
            selectedCategory === cat ? "bg-blue-100 text-blue-700" : "hover:bg-gray-100"
          )}
        >
          {cat}
        </button>
      ))}
    </aside>
  )
}
