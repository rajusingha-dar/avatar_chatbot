"""
Logging configuration for the application
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Create logs directory if it doesn't exist
Path("logs").mkdir(exist_ok=True)

# Configure root logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

# Create a custom logger
_logger = logging.getLogger("voice_avatar_chatbot")
_logger.setLevel(logging.DEBUG)

# Define formatter
_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create console handler
_console_handler = logging.StreamHandler()
_console_handler.setFormatter(_formatter)
_logger.addHandler(_console_handler)

# Create file handler
_file_handler = RotatingFileHandler(
    "logs/app.log", 
    maxBytes=10485760,  # 10MB
    backupCount=5
)
_file_handler.setFormatter(_formatter)
_logger.addHandler(_file_handler)

def get_logger(name=None):
    """
    Get the logger instance.
    If name is provided, returns a child logger with the given name.
    """
    if name:
        return _logger.getChild(name)
    return _logger