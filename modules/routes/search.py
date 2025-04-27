# modules/routes/search.py

"""
Search route handler with external API integration
"""

import json
import traceback
import requests
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import Optional
from modules.logger import get_logger
from modules.config import get_serper_api_key  # You'll need to add this to your config

# Setup API Router
router = APIRouter()
logger = get_logger("routes.search")

class SearchRequest(BaseModel):
    query: str
    type: Optional[str] = "search"  # search, news, places, images

@router.post("/api/search")
async def search(request: SearchRequest = Body(...)):
    """
    Perform a real-time search using Serper API (Google Search API)
    """
    try:
        logger.info(f"Search request received: {request.query[:30]}...")
        
        # Get Serper API key (you'll need to set this up)
        api_key = get_serper_api_key()
        if not api_key:
            logger.error("Serper API key not found")
            raise HTTPException(
                status_code=500,
                detail="Search API key not configured. Please set the SERPER_API_KEY environment variable."
            )

        # Call Serper API (Google Search API)
        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "q": request.query,
            "gl": "us",  # Geolocation (us, uk, etc)
            "hl": "en",  # Language
            "num": 5     # Number of results
        }
        
        search_type = request.type.lower()
        if search_type == "news":
            endpoint = "https://api.serper.dev/news"
        elif search_type == "places":
            endpoint = "https://api.serper.dev/places"
        elif search_type == "images":
            endpoint = "https://api.serper.dev/images"
        else:
            endpoint = "https://api.serper.dev/search"
        
        logger.debug(f"Calling search API: {endpoint}")
        response = requests.post(
            endpoint,
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Search successful with {len(result.get('organic', []))} results")
            return result
        else:
            logger.error(f"Search API error: {response.status_code} - {response.text}")
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Search API error: {response.text}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error performing search: {str(e)}"
        logger.error(error_msg)
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=error_msg)