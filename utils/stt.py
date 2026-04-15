# Speech-to-Text utility — uses Groq Whisper API (free, fast).
# No local GPU needed.


import os
import logging
from groq import Groq

logger = logging.getLogger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")


def transcribe_audio(audio_path: str) -> tuple[str, str]:
    
    try:
        client = Groq(api_key=GROQ_API_KEY)
        with open(audio_path, "rb") as f:
            transcription = client.audio.transcriptions.create(
                file=(os.path.basename(audio_path), f),
                model="whisper-large-v3",
                response_format="text",
            )
        return transcription.strip(), "groq:whisper-large-v3"
    except Exception as e:
        logger.error(f"Groq STT failed: {e}")
        return "", "groq:whisper-large-v3"
