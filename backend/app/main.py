"""
RSS Web Reader API - Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core import logger
from app.api import health, articles, feeds, stats

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="RSS Web Reader API",
        description="AI-powered RSS feed aggregator with Chinese summaries",
        version="1.0.0"
    )

    # CORS middleware for frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite dev server
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers
    app.include_router(health.router, tags=["health"])
    app.include_router(articles.router, prefix="/api/articles", tags=["articles"])
    app.include_router(feeds.router, prefix="/api/feeds", tags=["feeds"])
    app.include_router(stats.router, prefix="/api/stats", tags=["stats"])

    logger.info("app_started", version="1.0.0")
    return app

# Create app instance
app = create_app()
