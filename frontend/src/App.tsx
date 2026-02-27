import { useState } from 'react'
import { Layout } from './components/Layout'
import { Sidebar } from './components/Sidebar'
import { ArticleList } from './components/ArticleList'

function App() {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const [searchKeyword, setSearchKeyword] = useState('')

  return (
    <Layout onSearch={setSearchKeyword}>
      <div className="flex flex-col md:flex-row">
        <Sidebar
          selectedCategory={selectedCategory}
          onSelectCategory={setSelectedCategory}
        />
        <div className="flex-1">
          <ArticleList
            category={selectedCategory}
            keyword={searchKeyword || undefined}
          />
        </div>
      </div>
    </Layout>
  )
}

export default App
