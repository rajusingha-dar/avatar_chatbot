"""
Text-to-Speech (TTS) route handlers
"""
import traceback
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from modules.logger import get_logger
from io import BytesIO

router = APIRouter()
logger = get_logger("routes.tts")

@router.post("/api/tts")
async def text_to_speech(text: dict):
    """
    Convert text to speech and return audio file.
    """
    try:
        logger.info(f"Received text for TTS: {text}")

        # (Simulation) Generate dummy audio
        dummy_audio = BytesIO(b"This is dummy audio content.")

        return StreamingResponse(dummy_audio, media_type="audio/mpeg")
    
    except Exception as e:
        logger.error(f"Error in text-to-speech: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to generate audio.")
