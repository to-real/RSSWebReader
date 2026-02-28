import { useState } from 'react'
import { Layout } from './components/Layout'
import { Sidebar } from './components/Sidebar'
import { ArticleList } from './components/ArticleList'

function App() {
  const [selectedFeedId, setSelectedFeedId] = useState<number | null>(null)
  const [searchKeyword, setSearchKeyword] = useState('')

  return (
    <Layout onSearch={setSearchKeyword}>
      <div className="flex flex-col md:flex-row min-h-[calc(100vh-4rem)]">
        <Sidebar
          selectedFeedId={selectedFeedId}
          onSelectFeed={setSelectedFeedId}
        />
        <main className="flex-1 min-w-0" style={{ background: 'var(--bg-primary)' }}>
          <ArticleList
            feedId={selectedFeedId}
            keyword={searchKeyword || undefined}
          />
        </main>
      </div>
    </Layout>
  )
}

export default App
