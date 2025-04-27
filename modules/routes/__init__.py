"""
Routes package for the Voice Avatar Chatbot
"""
from fastapi import FastAPI
from modules.logger import get_logger

# Setup logger
logger = get_logger("routes")

def setup_routes(app: FastAPI):
    """
    Setup all API routes for the application
    
    Args:
        app: FastAPI application instance
    """
    try:
        # Import route modules
        from modules.routes import chat, search, test
        
        # Try to import text-to-speech module if available
        try:
            from modules.routes import text_to_speech
            app.include_router(text_to_speech.router)
            logger.info("Text-to-speech routes loaded")
        except ImportError:
            logger.warning("Text-to-speech module not available")
            
        # Try to import speech module if available
        try:
            from modules.routes import speech
            app.include_router(speech.router)
            logger.info("Speech routes loaded")
        except ImportError:
            logger.warning("Speech module not available")
        
        # Add main route handlers
        app.include_router(chat.router)
        app.include_router(search.router)
        app.include_router(test.router)
        
        logger.info("API routes configured successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error setting up routes: {str(e)}")
        return False