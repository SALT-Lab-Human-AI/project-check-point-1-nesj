import re
import os
from gtts import gTTS
from io import BytesIO
import base64

def clean_text_for_speech(text: str) -> str:
    """
    Clean text for TTS by removing emojis and special symbols
    while keeping natural speech flow
    """
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+", 
        flags=re.UNICODE
    )
    
    text = emoji_pattern.sub('', text)
    
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'_([^_]+)_', r'\1', text)
    
    text = text.replace('💊', 'medication')
    text = text.replace('🏥', '')
    text = text.replace('💬', '')
    
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def generate_speech_audio(text: str, slow: bool = True) -> bytes:
    """
    Generate speech audio from text using gTTS with a calm, clear voice
    
    Args:
        text: The text to convert to speech
        slow: If True, use slower speech rate (better for elderly users)
    
    Returns:
        Audio bytes in MP3 format
    """
    cleaned_text = clean_text_for_speech(text)
    
    if not cleaned_text:
        return None
    
    tts = gTTS(text=cleaned_text, lang='en', slow=slow)
    
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    
    return audio_buffer.read()

def text_to_audio_base64(text: str, slow: bool = True) -> str:
    """
    Convert text to base64 encoded audio for embedding in HTML
    
    Args:
        text: The text to convert to speech
        slow: If True, use slower speech rate
    
    Returns:
        Base64 encoded audio string
    """
    audio_bytes = generate_speech_audio(text, slow=slow)
    
    if audio_bytes:
        return base64.b64encode(audio_bytes).decode()
    
    return None
