# modules/models.py

"""
Pydantic models for request and response validation
"""

from pydantic import BaseModel
from typing import List

# Define a single message structure (used in chat history)
class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str  # The text content of the message

# Define the full chat request expected by the /api/chat endpoint
class ChatRequest(BaseModel):
    messages: List[Message]
