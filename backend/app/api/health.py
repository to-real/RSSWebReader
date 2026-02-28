from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
@router.get("/api/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
    }
