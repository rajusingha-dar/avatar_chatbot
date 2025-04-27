# """
# Main route handlers
# """
# import time
# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse
# from modules.logger import get_logger

# # Setup logger
# logger = get_logger("routes.main")

# def add_main_routes(app: FastAPI):
#     """Add main routes to the app"""
    
#     @app.middleware("http")
#     async def log_requests(request: Request, call_next):
#         """Middleware to log all requests and responses"""
#         request_id = f"req-{time.time()}"
#         logger.info(f"Request {request_id} started: {request.method} {request.url.path}")
        
#         # Process the request and get the response
#         try:
#             response = await call_next(request)
#             logger.info(f"Request {request_id} completed with status code: {response.status_code}")
#             return response
#         except Exception as e:
#             logger.error(f"Request {request_id} failed with error: {str(e)}")
#             return JSONResponse(
#                 status_code=500,
#                 content={"detail": "Internal server error"}
#             )
    
#     @app.get("/api/test")
#     async def test_endpoint():
#         """Test endpoint to verify API is working"""
#         logger.info("Test endpoint accessed")
#         return {
#             "status": "ok", 
#             "message": "API is working", 
#             "timestamp": time.time()
#         }



"""
Voice Avatar Chatbot - Main application file
"""

import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Import modules
from modules.config import setup_environment, HOST, PORT, DEBUG
from modules.logger import get_logger
from modules.routes import chat, search, text_to_speech, test

# Setup logger
logger = get_logger("voice_avatar_chatbot")

# Create FastAPI app
app = FastAPI(
    title="Voice Avatar Chatbot",
    description="A chatbot with voice input/output and avatar visualization",
    version="1.0.0"
)

# Load configuration
if not setup_environment():
    logger.error("Failed to load configuration. Exiting...")
    exit(1)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify exact origins
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API routes
app.include_router(chat.router)
app.include_router(search.router)
app.include_router(text_to_speech.router)
app.include_router(test.router)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the main application page"""
    logger.info("Root endpoint accessed - serving index.html")
    
    # Serve the index.html file
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        logger.info(f"Serving {index_path} file")
        return FileResponse(index_path)
    else:
        logger.error(f"File not found: {index_path}")
        raise HTTPException(status_code=404, detail="Page not found")

# Run the application when executed directly
if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on {HOST}:{PORT}")
    uvicorn.run("app:app", host=HOST, port=PORT, reload=DEBUG)