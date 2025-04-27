"""
Configuration module for the Voice Avatar Chatbot
"""

import os
import sys
from dotenv import load_dotenv
from modules.logger import get_logger

logger = get_logger("config")

# Load environment variables from .env file
load_dotenv()

def get_env_variable(key, default=None, required=False):
    """
    Get an environment variable, with optional default value
    and required flag for validation
    """
    value = os.getenv(key, default)
    if required and value is None:
        logger.error(f"Required environment variable {key} is not set")
        sys.exit(1)
    return value

def get_openai_api_key():
    """Get OpenAI API key from environment variables"""
    return get_env_variable("OPENAI_API_KEY", required=True)

def get_openai_key():
    """Alias for get_openai_api_key to maintain compatibility with older code"""
    return get_openai_api_key()

def get_tavily_api_key():
    """Get Tavily API key from environment variables"""
    return get_env_variable("TAVILY_API_KEY")

def setup_environment():
    """
    Setup environment and validate configuration
    Compatibility function for existing codebase
    """
    return load_config()

def load_config():
    """
    Load and validate all required configuration
    """
    try:
        # Check required API keys
        missing_keys = []
        
        # Check OpenAI API key
        openai_api_key = get_openai_api_key()
        if not openai_api_key:
            missing_keys.append("OPENAI_API_KEY")
            
        # Check Tavily API key
        tavily_api_key = get_tavily_api_key()
        if not tavily_api_key:
            missing_keys.append("TAVILY_API_KEY")
            
        # Log any missing keys
        if missing_keys:
            logger.warning(f"Missing API keys: {', '.join(missing_keys)}")
        
        logger.info("Environment variables loaded successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error loading configuration: {str(e)}")
        return False

# Application configuration
DEBUG = get_env_variable("DEBUG", default="False").lower() in ["true", "1", "yes"]
PORT = int(get_env_variable("PORT", default="8000"))
HOST = get_env_variable("HOST", default="0.0.0.0")

# OpenAI Configuration
OPENAI_MODEL = get_env_variable("OPENAI_MODEL", default="gpt-3.5-turbo")
MAX_TOKENS = int(get_env_variable("MAX_TOKENS", default="500"))
TEMPERATURE = float(get_env_variable("TEMPERATURE", default="0.7"))

# Default system message for chat
DEFAULT_SYSTEM_MESSAGE = get_env_variable(
    "DEFAULT_SYSTEM_MESSAGE", 
    default="You are a helpful, friendly, and intelligent AI assistant."
)