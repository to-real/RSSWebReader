import { useState } from 'react'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          RSS Web Reader
        </h1>
        <p className="text-gray-600 mb-8">
          RSS 聚合 + AI 摘要 + 中文解读
        </p>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-700">
            Frontend initialized successfully!
          </p>
        </div>
      </div>
    </div>
  )
}

export default App
