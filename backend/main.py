from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core import logger
from app.api import health, articles, feeds, stats

app = FastAPI(title="RSS Web Reader API")

# CORS middleware - needed for production when frontend/backend are on different domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["health"])
app.include_router(stats.router, prefix="/api", tags=["stats"])
app.include_router(articles.router, prefix="/api/articles", tags=["articles"])
app.include_router(feeds.router, prefix="/api/feeds", tags=["feeds"])

@app.on_event("startup")
async def startup():
    logger.info("api_started")

@app.on_event("shutdown")
async def shutdown():
    logger.info("api_stopped")
