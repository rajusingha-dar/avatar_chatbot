# # modules/routes/chat.py

# """
# Text generation route handlers with OpenAI integration
# """

# import json
# import traceback
# import requests
# from fastapi import APIRouter, HTTPException, Body
# from modules.logger import get_logger
# from modules.config import get_openai_key
# from modules.models import ChatRequest

# # Setup API Router
# router = APIRouter()
# logger = get_logger("routes.chat")

# @router.post("/api/chat")
# async def generate_text(request: ChatRequest = Body(...)):
#     """
#     Generate text response using OpenAI's GPT API
#     """
#     try:
#         # Log incoming messages safely
#         safe_messages = [
#             {
#                 "role": msg.role,
#                 "content": f"{msg.content[:30]}..." if len(msg.content) > 30 else msg.content
#             }
#             for msg in request.messages
#         ]
#         logger.info(f"Generate text request received with {len(request.messages)} messages")
#         logger.debug(f"Messages content: {json.dumps(safe_messages)}")

#         # Load OpenAI API key
#         openai_key = get_openai_key()
#         if not openai_key:
#             logger.error("OpenAI API key not found")
#             raise HTTPException(
#                 status_code=500,
#                 detail="OpenAI API key not configured. Please set the OPENAI_API_KEY environment variable."
#             )

#         headers = {
#             "Authorization": f"Bearer {openai_key}",
#             "Content-Type": "application/json"
#         }

#         # Prepare the messages list with a system prompt
#         messages = [
#             {
#                 "role": "system",
#                 "content": (
#                     "You are a helpful, friendly AI assistant. "
#                     "Always respond in English. "
#                     "Be polite, conversational, and informative."
#                 )
#             }
#         ]

#         # Add user and assistant message history
#         for msg in request.messages:
#             messages.append({
#                 "role": msg.role,
#                 "content": msg.content
#             })

#         payload = {
#             "model": "gpt-4-turbo-preview",
#             "messages": messages,
#             "max_tokens": 500,
#             "temperature": 0.7,
#             "top_p": 0.9,
#             "frequency_penalty": 0.0,
#             "presence_penalty": 0.6
#         }

#         logger.debug("Sending request to OpenAI Chat API")

#         response = requests.post(
#             "https://api.openai.com/v1/chat/completions",
#             headers=headers,
#             json=payload,
#             timeout=30
#         )

#         logger.debug(f"OpenAI Chat API response status: {response.status_code}")

#         if response.status_code == 200:
#             result = response.json()
#             if result.get("choices") and len(result["choices"]) > 0:
#                 content = result["choices"][0].get("message", {}).get("content", "")
#                 logger.info(f"Successfully generated text: '{content[:30]}...'")
#             return result
#         else:
#             error_msg = f"Error from OpenAI API: {response.text}"
#             logger.error(error_msg)
#             raise HTTPException(
#                 status_code=response.status_code,
#                 detail=error_msg
#             )

#     except HTTPException as he:
#         logger.error(f"HTTP Exception in generate-text: {str(he)}")
#         raise

#     except Exception as e:
#         error_msg = f"Error generating text: {str(e)}"
#         logger.error(error_msg)
#         logger.error(f"Traceback: {traceback.format_exc()}")
#         raise HTTPException(status_code=500, detail=error_msg)



# modules/routes/chat.py

"""
Text generation route handlers with OpenAI integration
"""

import json
import traceback
import requests
import re
from fastapi import APIRouter, HTTPException, Body
from modules.logger import get_logger
from modules.config import get_openai_key, OPENAI_MODEL, MAX_TOKENS, TEMPERATURE
from modules.models import ChatRequest
from modules.routes.search import SearchRequest

# Setup API Router
router = APIRouter()
logger = get_logger("routes.chat")

# Pattern to detect real-time queries
REAL_TIME_PATTERNS = [
    r"(?:what|how) is (?:the )?(?:current|today'?s?|latest|present|right now) (.*?)(?: in | at | for | on )(.*?)(?:\?|$)",
    r"(?:what|how) (?:is|are) (?:the )?(?:current|today'?s?|latest|present|right now) (.*?)(?:\?|$)",
    r"what (?:is|are) (?:the )?(?:weather|temperature|forecast) (?:like )?(?:in|at|for) (.*?)(?:\?|$)",
    r"what time is it(?: in| at) (.*?)(?:\?|$)",
    r"what is happening(?: in| at) (.*?)(?:\?|$)",
    r"latest news(?: about| on| in| regarding) (.*?)(?:\?|$)",
]

@router.post("/api/chat")
async def generate_text(request: ChatRequest = Body(...)):
    """
    Generate text response using OpenAI's GPT API
    """
    try:
        # Log incoming messages safely
        safe_messages = [
            {
                "role": msg.role,
                "content": f"{msg.content[:30]}..." if len(msg.content) > 30 else msg.content
            }
            for msg in request.messages
        ]
        logger.info(f"Generate text request received with {len(request.messages)} messages")
        logger.debug(f"Messages content: {json.dumps(safe_messages)}")

        # Extract the latest user message
        latest_user_message = next((msg.content for msg in reversed(request.messages) 
                                  if msg.role == "user"), None)
        
        # If we have a user message, check if it requires real-time information
        search_results = None
        if latest_user_message:
            # Check for real-time query patterns
            for pattern in REAL_TIME_PATTERNS:
                if re.search(pattern, latest_user_message, re.IGNORECASE):
                    logger.info(f"Detected real-time query: {latest_user_message}")
                    try:
                        # Perform search
                        search_request = SearchRequest(query=latest_user_message)
                        search_response = requests.post(
                            "http://localhost:8000/api/search",  # Local call to our own API
                            json={"query": latest_user_message},
                            timeout=10
                        )
                        
                        if search_response.status_code == 200:
                            search_results = search_response.json()
                            logger.info("Search completed successfully")
                        else:
                            logger.warning(f"Search failed with status {search_response.status_code}")
                    except Exception as e:
                        logger.error(f"Error performing search: {str(e)}")
                    
                    # No need to check other patterns
                    break

        # Load OpenAI API key
        openai_key = get_openai_key()
        if not openai_key:
            logger.error("OpenAI API key not found")
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key not configured. Please set the OPENAI_API_KEY environment variable."
            )

        headers = {
            "Authorization": f"Bearer {openai_key}",
            "Content-Type": "application/json"
        }

        # Prepare the messages list with a system prompt
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful, friendly AI assistant integrated with a voice interface. "
                    "Always respond in English. Keep responses concise and conversational. "
                    "Be polite, engaging, and informative. Speak as if you're having a natural conversation."
                )
            }
        ]

        # If we have search results, add them as context
        if search_results:
            search_context = "I've searched for real-time information and found these results:\n\n"
            
            # Add organic search results
            if "organic" in search_results:
                for i, result in enumerate(search_results["organic"][:3], 1):
                    title = result.get("title", "No title")
                    snippet = result.get("snippet", "No description")
                    search_context += f"{i}. {title}: {snippet}\n"
            
            # Add knowledge graph if available
            if "knowledgeGraph" in search_results:
                kg = search_results["knowledgeGraph"]
                if "title" in kg:
                    search_context += f"\nKnowledge Graph: {kg.get('title')}\n"
                    if "description" in kg:
                        search_context += f"Description: {kg.get('description')}\n"
                    
                    # Add attributes
                    if "attributes" in kg:
                        for key, value in kg["attributes"].items():
                            search_context += f"{key}: {value}\n"
            
            # Add answer box if available
            if "answerBox" in search_results:
                answer = search_results["answerBox"]
                if "answer" in answer:
                    search_context += f"\nFeatured Answer: {answer.get('answer')}\n"
                elif "snippet" in answer:
                    search_context += f"\nFeatured Snippet: {answer.get('snippet')}\n"
                    
            # Add weather if available
            if "weather" in search_results:
                weather = search_results["weather"]
                if "temperature" in weather:
                    search_context += f"\nWeather: {weather.get('temperature')}, {weather.get('condition')}\n"
            
            # Add as a system message
            search_context += "\n\nUse this information to answer the user's question accurately and naturally."
            messages.append({
                "role": "system", 
                "content": search_context
            })

        # Add user and assistant message history
        for msg in request.messages:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })

        payload = {
            "model": OPENAI_MODEL,
            "messages": messages,
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
            "top_p": 0.9,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.6
        }

        logger.debug("Sending request to OpenAI Chat API")

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )

        logger.debug(f"OpenAI Chat API response status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            if result.get("choices") and len(result["choices"]) > 0:
                content = result["choices"][0].get("message", {}).get("content", "")
                logger.info(f"Successfully generated text: '{content[:30]}...'")
            return result
        else:
            error_msg = f"Error from OpenAI API: {response.text}"
            logger.error(error_msg)
            raise HTTPException(
                status_code=response.status_code,
                detail=error_msg
            )

    except HTTPException as he:
        logger.error(f"HTTP Exception in generate-text: {str(he)}")
        raise

    except Exception as e:
        error_msg = f"Error generating text: {str(e)}"
        logger.error(error_msg)
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=error_msg)