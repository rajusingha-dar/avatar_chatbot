"""
Main route handlers
"""
import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from modules.logger import get_logger

# Setup logger
logger = get_logger("routes.main")

def add_main_routes(app: FastAPI):
    """Add main routes to the app"""
    
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """Middleware to log all requests and responses"""
        request_id = f"req-{time.time()}"
        logger.info(f"Request {request_id} started: {request.method} {request.url.path}")
        
        # Process the request and get the response
        try:
            response = await call_next(request)
            logger.info(f"Request {request_id} completed with status code: {response.status_code}")
            return response
        except Exception as e:
            logger.error(f"Request {request_id} failed with error: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"}
            )
    
    @app.get("/api/test")
    async def test_endpoint():
        """Test endpoint to verify API is working"""
        logger.info("Test endpoint accessed")
        return {
            "status": "ok", 
            "message": "API is working", 
            "timestamp": time.time()
        }