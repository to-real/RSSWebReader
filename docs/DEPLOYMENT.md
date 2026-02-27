# Deployment Guide

## Railway Deployment

1. Create new project on Railway
2. Add PostgreSQL database
3. Set environment variables:
   - `DATABASE_URL`
   - `CLAUDE_API_KEY`
   - `FETCH_INTERVAL_MINUTES=30`
4. Push to GitHub
5. Connect GitHub repo to Railway
6. Deploy!

## Environment Variables

See `.env.example` for full list.
