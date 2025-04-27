"""
Search route handler with Tavily API integration through LangChain
"""

import json
import traceback
import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import Optional, Dict, Any
from modules.logger import get_logger
from modules.config import get_env_variable

# Import LangChain's Tavily tool
from langchain_community.tools.tavily_search import TavilySearchResults

# Setup API Router
router = APIRouter()
logger = get_logger("routes.search")

# Simple in-memory cache to avoid repeated identical searches
# Format: {query: {timestamp: timestamp, results: results}}
SEARCH_CACHE = {}
CACHE_TTL = 300  # Cache results for 5 minutes (300 seconds)

class SearchRequest(BaseModel):
    query: str
    search_depth: Optional[str] = "basic"  # basic or advanced

async def search(request: SearchRequest):
    """
    Functional implementation of search logic that can be called directly
    or via the HTTP endpoint
    """
    try:
        query = request.query
        logger.info(f"Search request received: {query[:30]}...")
        
        # Check cache first
        import time
        current_time = time.time()
        
        if query in SEARCH_CACHE:
            cache_entry = SEARCH_CACHE[query]
            # If cache is still valid (not expired)
            if current_time - cache_entry["timestamp"] < CACHE_TTL:
                logger.info(f"Using cached search results for query: {query[:30]}...")
                return cache_entry["results"]
        
        # Make sure Tavily API key is defined in environment variables
        # The TavilySearchResults class reads from TAVILY_API_KEY env var automatically
        tavily_api_key = get_env_variable("TAVILY_API_KEY")
        if not tavily_api_key:
            logger.error("Tavily API key not found")
            raise HTTPException(
                status_code=500,
                detail="Tavily API key not configured. Please set the TAVILY_API_KEY environment variable."
            )

        # Initialize Tavily search tool
        search_tool = TavilySearchResults(
            search_depth=request.search_depth,  # "basic" or "advanced"
            k=5  # Number of results to return
        )
        
        logger.debug(f"Calling Tavily search API with query: {query}")
        
        # Execute the search in a separate thread to avoid blocking
        try:
            # Run the blocking search in a thread pool
            with ThreadPoolExecutor() as executor:
                results = await asyncio.get_event_loop().run_in_executor(
                    executor, 
                    search_tool.invoke,
                    query
                )
                
            logger.info(f"Search successful with {len(results)} results")
            
            # Format the response to match your frontend expectations
            formatted_results = {
                "organic": [],
                "query": query,
                "searchDepth": request.search_depth
            }
            
            for item in results:
                formatted_results["organic"].append({
                    "title": item.get("title", ""),
                    "link": item.get("url", ""),
                    "snippet": item.get("content", ""),
                    "source": item.get("source", "Tavily")
                })
            
            # Cache the results for future use
            SEARCH_CACHE[query] = {
                "timestamp": current_time,
                "results": formatted_results
            }
            
            # Cleanup old cache entries
            cleanup_cache(current_time)
                
            return formatted_results
            
        except Exception as e:
            logger.error(f"Tavily search error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Tavily search error: {str(e)}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error performing search: {str(e)}"
        logger.error(error_msg)
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=error_msg)

def cleanup_cache(current_time):
    """Remove expired entries from cache"""
    global SEARCH_CACHE
    keys_to_remove = []
    
    for key, cache_entry in SEARCH_CACHE.items():
        if current_time - cache_entry["timestamp"] > CACHE_TTL:
            keys_to_remove.append(key)
    
    for key in keys_to_remove:
        del SEARCH_CACHE[key]

@router.post("/api/search")
async def search_endpoint(request: SearchRequest = Body(...)):
    """
    HTTP endpoint for the search functionality
    This now just wraps the functional implementation
    """
    return await search(request)