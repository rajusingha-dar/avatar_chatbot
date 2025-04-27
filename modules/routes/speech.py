"""
Speech-to-Text (STT) route handlers
"""
import traceback
from fastapi import APIRouter, UploadFile, File, HTTPException
from modules.logger import get_logger

router = APIRouter()
logger = get_logger("routes.speech")

@router.post("/api/speech")
async def speech_to_text(audio: UploadFile = File(...)):
    """
    Receive audio file and return transcribed text.
    """
    try:
        logger.info(f"Received audio file: {audio.filename}")

        # (Simulation) Transcribe here using your model
        # For now, just return a dummy text
        transcribed_text = "Hello, this is a dummy transcription."

        return {"text": transcribed_text}
    
    except Exception as e:
        logger.error(f"Error in speech-to-text: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to transcribe audio.")
