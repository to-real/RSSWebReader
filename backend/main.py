"""
Compatibility entrypoint for `uvicorn main:app`.

Single source of truth lives in app.main.
"""
from app.main import app

__all__ = ["app"]
