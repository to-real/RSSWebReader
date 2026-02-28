# RSS Web Reader

RSS 聚合 + AI 摘要 + 中文解读

## Features

- 📡 聚合 92 个顶级技术博客
- 🤖 Claude AI 生成中文摘要
- 📱 响应式设计，支持移动端
- 🔍 实时搜索文章
- 🏷️ 智能关键词标签

## Quick Start

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Edit .env with your Claude API key
python scripts/init.py  # Initialize database and fetch articles
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Visit http://localhost:3000

## Development

### Start API server

```bash
cd backend
uvicorn main:app --reload
```

### Start worker (RSS fetcher + AI processor)

```bash
cd backend
python -m app.tasks.scheduler
```

## Deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
See [docs/FEED_TAXONOMY.md](docs/FEED_TAXONOMY.md) for manual source classification workflow.

## License

MIT
