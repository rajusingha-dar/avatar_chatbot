"""
Main FastAPI application for Voice Avatar Chatbot
"""
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
from pathlib import Path
import traceback

# Import modules
from modules.config import setup_environment
from modules.logger import get_logger
from modules.routes import setup_routes  # only this
from modules.templates.fallback_html import FALLBACK_HTML

# Setup logger
logger = get_logger()

# Setup environment
setup_environment()

# Initialize FastAPI
app = FastAPI(title="Voice Avatar Chatbot API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Default route for serving the frontend
@app.get("/")
async def root():
    """Serve the main HTML page directly"""
    try:
        logger.info("Root endpoint accessed - serving index.html")
        
        index_path = Path("static/index.html")
        if index_path.exists():
            logger.info("Serving static/index.html file")
            return HTMLResponse(content=open(index_path, "r").read())
        
        logger.info("Static file not found, using embedded HTML")
        return HTMLResponse(content=FALLBACK_HTML)
    
    except Exception as e:
        logger.error(f"Error serving index.html: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return HTMLResponse(content=FALLBACK_HTML)

# Add routes (imported)
setup_routes(app)

# Mount static files
try:
    static_dir = Path("static")
    if not static_dir.exists():
        logger.warning("Static directory not found. Creating it.")
        static_dir.mkdir(exist_ok=True)
    
    app.mount("/static", StaticFiles(directory="static"), name="static")
    logger.info("Static files mounted successfully")
except Exception as e:
    logger.error(f"Error mounting static files: {str(e)}")
    logger.info("Will use fallback HTML instead")

# Start uvicorn
if __name__ == "__main__":
    logger.info("Starting Voice Avatar Chatbot server")
    try:
        uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
    except Exception as e:
        logger.critical(f"Failed to start server: {str(e)}")
        logger.critical(f"Traceback: {traceback.format_exc()}")
