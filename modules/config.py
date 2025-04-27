# """
# Configuration and environment setup
# """
# import os
# from dotenv import load_dotenv
# from pathlib import Path
# from modules.logger import get_logger

# # Setup logger
# logger = get_logger("config")

# def setup_environment():
#     """Load environment variables from .env file"""
#     env_path = Path('.') / '.env'
#     load_dotenv(dotenv_path=env_path)
#     logger.info("Environment variables loaded successfully")
    
#     # Check for API keys
#     api_keys_status = check_api_keys()
#     if api_keys_status:
#         logger.info("API keys loaded successfully")
#     else:
#         logger.warning("Some API keys are missing")

# def check_api_keys():
#     """Check if all required API keys are present"""
#     required_keys = ['OPENAI_API_KEY', 'ELEVENLABS_API_KEY']
#     all_present = True
    
#     for key in required_keys:
#         if not os.getenv(key):
#             logger.warning(f"Missing API key: {key}")
#             all_present = False
    
#     return all_present

# def get_openai_key():
#     """Get OpenAI API key from environment variables"""
#     api_key = os.getenv('OPENAI_API_KEY')
#     if not api_key:
#         logger.error("OpenAI API key not found in environment variables")
#     return api_key

# def get_elevenlabs_key():
#     """Get ElevenLabs API key from environment variables"""
#     api_key = os.getenv('ELEVENLABS_API_KEY')
#     if not api_key:
#         logger.error("ElevenLabs API key not found in environment variables")
#     return api_key


# modules/config.py

"""
Configuration and environment setup
"""

import os
import logging
from dotenv import load_dotenv
from modules.logger import get_logger

# Setup logger
logger = get_logger("config")

def setup_environment():
    """
    Load environment variables from .env file
    """
    try:
        # Try to load from .env file
        load_dotenv()
        logger.info("Environment variables loaded successfully")
        
        # Check for required API keys
        _check_api_keys()
        
    except Exception as e:
        logger.error(f"Error loading environment: {str(e)}")
        # Continue anyway - we'll check for keys when needed

def _check_api_keys():
    """
    Check that required API keys are present
    """
    required_keys = {
        'OPENAI_API_KEY': get_openai_key(),
        'SERPER_API_KEY': get_serper_api_key()
    }
    
    missing_keys = [key for key, value in required_keys.items() if not value]
    
    if missing_keys:
        logger.warning(f"Missing API keys: {', '.join(missing_keys)}")
    else:
        logger.info("API keys loaded successfully")

def get_openai_key():
    """
    Get OpenAI API key from environment
    """
    return os.getenv("OPENAI_API_KEY")

def get_serper_api_key():
    """
    Get Serper API key from environment
    """
    return os.getenv("SERPER_API_KEY")

# Add additional configuration settings here
# Example: model settings, etc.
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "500"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))