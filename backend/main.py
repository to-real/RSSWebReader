from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title="RSS Web Reader API")

@app.get("/health")
async def health():
    return {"status": "ok", "db": "connected", "last_fetch": None}

@app.get("/")
async def root():
    return {"message": "RSS Web Reader API"}
