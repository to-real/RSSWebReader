import { ReactNode } from 'react'
import { useState, useEffect } from 'react'
import { useDebounce } from '../hooks/useDebounce'

interface LayoutProps {
  children: ReactNode
  onSearch: (keyword: string) => void
}

export function Layout({ children, onSearch }: LayoutProps) {
  const [searchInput, setSearchInput] = useState('')
  const debouncedSearch = useDebounce(searchInput, 300)

  useEffect(() => {
    onSearch(debouncedSearch)
  }, [debouncedSearch, onSearch])

  return (
    <div className="min-h-screen bg-white">
      <header className="bg-white border-b sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl font-bold">RSS Web Reader</h1>
          <input
            type="text"
            placeholder="搜索文章标题..."
            value={searchInput}
            onChange={e => setSearchInput(e.target.value)}
            className="px-4 py-2 border rounded-lg w-64 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </header>

      <main className="max-w-6xl mx-auto">
        {children}
      </main>
    </div>
  )
}
