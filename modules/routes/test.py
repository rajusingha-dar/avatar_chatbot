"""
Test route handler for API status checks
"""
import time
from fastapi import APIRouter
from modules.logger import get_logger

# Setup API Router
router = APIRouter()
logger = get_logger("routes.test")

@router.get("/api/test")
async def test_api():
    """
    Test endpoint to verify API is working
    """
    logger.info("API test endpoint accessed")
    return {
        "status": "ok",
        "message": "API is working correctly",
        "timestamp": time.time()
    }

@router.get("/api/test/search")
async def test_search():
    """
    Test endpoint to verify that the search functionality is configured
    """
    logger.info("Search test endpoint accessed")
    
    from modules.config import get_tavily_api_key
    
    search_api_key = get_tavily_api_key()
    status = "ok" if search_api_key else "error"
    message = "Tavily search API key found" if search_api_key else "Tavily search API key not configured"
    
    return {
        "status": status,
        "message": message,
        "timestamp": time.time()
    }