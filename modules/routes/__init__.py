# """
# Initialize all routes for the Voice Avatar Chatbot
# """

# from fastapi import FastAPI
# from modules.logger import get_logger

# # Import route modules
# from modules.routes import chat, speech, tts
# from modules.routes.test import router as test_router

# logger = get_logger("routes")

# def setup_routes(app: FastAPI):
#     """
#     Setup all API routes
#     """
#     # Include all route modules
#     app.include_router(chat.router)
#     app.include_router(speech.router)
#     app.include_router(tts.router)
#     app.include_router(test_router)
    
#     logger.info("API routes configured successfully")



"""
Initialize all routes for the Voice Avatar Chatbot
"""

from fastapi import FastAPI
from modules.logger import get_logger

# Import route modules
from modules.routes import chat, speech, tts, test
from modules.routes.search import router as search_router

logger = get_logger("routes")

def setup_routes(app: FastAPI):
    """
    Setup all API routes
    """
    # Include all route modules
    app.include_router(chat.router)
    app.include_router(speech.router)
    app.include_router(tts.router)
    app.include_router(test.router)
    app.include_router(search_router)
    
    logger.info("API routes configured successfully")