import { useState } from 'react'
import { Layout } from './components/Layout'
import { Sidebar } from './components/Sidebar'
import { ArticleList } from './components/ArticleList'

function App() {
  const [selectedFeedId, setSelectedFeedId] = useState<number | null>(null)
  const [searchKeyword, setSearchKeyword] = useState('')

  return (
    <Layout onSearch={setSearchKeyword}>
      <div className="flex flex-col md:flex-row">
        <Sidebar
          selectedFeedId={selectedFeedId}
          onSelectFeed={setSelectedFeedId}
        />
        <div className="flex-1">
          <ArticleList
            feedId={selectedFeedId}
            keyword={searchKeyword || undefined}
          />
        </div>
      </div>
    </Layout>
  )
}

export default App
