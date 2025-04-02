import os
import requests
from gtts import gTTS

AUDIOBOOK_FOLDER = "static/audiobooks"
os.makedirs(AUDIOBOOK_FOLDER, exist_ok=True)

def generate_audiobook(book_id, text_url):
    """
    Fetches book text from Gutenberg and converts it to an audiobook.
    """
    try:
        response = requests.get(text_url)
        response.raise_for_status()
        book_text = response.text[:500]  # Limiting to the first 500 chars for demo

        tts = gTTS(book_text, lang="en")
        audio_path = os.path.join(AUDIOBOOK_FOLDER, f"{book_id}.mp3")
        tts.save(audio_path)
        
        return f"/audio/{book_id}"
    
    except Exception as e:
        print("Error generating audiobook:", e)
        return None
