# modules/routes/test.py

"""
Test route to check if API is responsive
"""

from fastapi import APIRouter
from modules.logger import get_logger

# Setup API Router
router = APIRouter()
logger = get_logger("routes.test")

@router.get("/api/test")
async def test_api():
    """
    Simple endpoint to test API connectivity
    """
    logger.info("API test endpoint accessed")
    return {"status": "ok", "message": "API is working"}