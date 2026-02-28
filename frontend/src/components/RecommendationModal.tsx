import { useState } from 'react'

interface RecommendationModalProps {
  isOpen: boolean
  onClose: () => void
}

export function RecommendationModal({ isOpen, onClose }: RecommendationModalProps) {
  const [feedUrl, setFeedUrl] = useState('')
  const [feedName, setFeedName] = useState('')
  const [reason, setReason] = useState('')
  const [contact, setContact] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [message, setMessage] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!feedUrl.trim()) return

    setSubmitting(true)
    try {
      const res = await fetch('/api/recommendations/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          feed_url: feedUrl.trim(),
          feed_name: feedName.trim() || null,
          reason: reason.trim() || null,
          contact: contact.trim() || null,
        }),
      })
      const data = await res.json()
      setMessage(data.message)
      if (data.success) {
        setTimeout(() => {
          setFeedUrl('')
          setFeedName('')
          setReason('')
          setContact('')
          setMessage('')
          onClose()
        }, 2000)
      }
    } catch {
      setMessage('提交失败，请稍后重试')
    } finally {
      setSubmitting(false)
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Modal */}
      <div
        className="relative w-full max-w-md rounded-2xl p-6 animate-fade-in"
        style={{
          background: 'var(--bg-primary)',
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        }}
      >
        <h2
          className="text-xl font-semibold mb-4"
          style={{ color: 'var(--fg-primary)' }}
        >
          推荐 RSS 源
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Feed URL */}
          <div>
            <label
              className="block text-sm font-medium mb-1.5"
              style={{ color: 'var(--fg-secondary)' }}
            >
              RSS 地址 *
            </label>
            <input
              type="url"
              value={feedUrl}
              onChange={(e) => setFeedUrl(e.target.value)}
              placeholder="https://example.com/feed.xml"
              required
              className="w-full px-3.5 py-2.5 rounded-xl text-sm outline-none transition-shadow"
              style={{
                background: 'var(--bg-secondary)',
                color: 'var(--fg-primary)',
                boxShadow: 'inset 0 0 0 1px var(--border)',
              }}
              onFocus={(e) => e.target.style.boxShadow = 'inset 0 0 0 1.5px var(--accent)'}
              onBlur={(e) => e.target.style.boxShadow = 'inset 0 0 0 1px var(--border)'}
            />
          </div>

          {/* Feed Name */}
          <div>
            <label
              className="block text-sm font-medium mb-1.5"
              style={{ color: 'var(--fg-secondary)' }}
            >
              源名称（可选）
            </label>
            <input
              type="text"
              value={feedName}
              onChange={(e) => setFeedName(e.target.value)}
              placeholder="例如：技术博客"
              className="w-full px-3.5 py-2.5 rounded-xl text-sm outline-none transition-shadow"
              style={{
                background: 'var(--bg-secondary)',
                color: 'var(--fg-primary)',
                boxShadow: 'inset 0 0 0 1px var(--border)',
              }}
              onFocus={(e) => e.target.style.boxShadow = 'inset 0 0 0 1.5px var(--accent)'}
              onBlur={(e) => e.target.style.boxShadow = 'inset 0 0 0 1px var(--border)'}
            />
          </div>

          {/* Reason */}
          <div>
            <label
              className="block text-sm font-medium mb-1.5"
              style={{ color: 'var(--fg-secondary)' }}
            >
              推荐理由（可选）
            </label>
            <textarea
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              placeholder="为什么推荐这个源？"
              rows={2}
              className="w-full px-3.5 py-2.5 rounded-xl text-sm outline-none transition-shadow resize-none"
              style={{
                background: 'var(--bg-secondary)',
                color: 'var(--fg-primary)',
                boxShadow: 'inset 0 0 0 1px var(--border)',
              }}
              onFocus={(e) => e.target.style.boxShadow = 'inset 0 0 0 1.5px var(--accent)'}
              onBlur={(e) => e.target.style.boxShadow = 'inset 0 0 0 1px var(--border)'}
            />
          </div>

          {/* Contact */}
          <div>
            <label
              className="block text-sm font-medium mb-1.5"
              style={{ color: 'var(--fg-secondary)' }}
            >
              联系方式（可选）
            </label>
            <input
              type="text"
              value={contact}
              onChange={(e) => setContact(e.target.value)}
              placeholder="邮箱，用于回复审核结果"
              className="w-full px-3.5 py-2.5 rounded-xl text-sm outline-none transition-shadow"
              style={{
                background: 'var(--bg-secondary)',
                color: 'var(--fg-primary)',
                boxShadow: 'inset 0 0 0 1px var(--border)',
              }}
              onFocus={(e) => e.target.style.boxShadow = 'inset 0 0 0 1.5px var(--accent)'}
              onBlur={(e) => e.target.style.boxShadow = 'inset 0 0 0 1px var(--border)'}
            />
          </div>

          {/* Message */}
          {message && (
            <div
              className="px-4 py-3 rounded-xl text-sm"
              style={{
                background: 'linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%)',
                color: '#065f46',
              }}
            >
              {message}
            </div>
          )}

          {/* Buttons */}
          <div className="flex gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2.5 rounded-xl text-sm font-medium transition-colors"
              style={{
                background: 'var(--bg-tertiary)',
                color: 'var(--fg-secondary)',
              }}
            >
              取消
            </button>
            <button
              type="submit"
              disabled={submitting || !feedUrl.trim()}
              className="flex-1 px-4 py-2.5 rounded-xl text-sm font-medium transition-opacity disabled:opacity-50"
              style={{
                background: 'var(--accent)',
                color: 'white',
              }}
            >
              {submitting ? '提交中...' : '提交推荐'}
            </button>
          </div>
        </form>

        {/* Close button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-lg transition-colors"
          style={{ color: 'var(--fg-tertiary)' }}
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  )
}
