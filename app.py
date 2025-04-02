import requests
import os
from gtts import gTTS
from flask import Flask, render_template, send_file, url_for, request, jsonify
from utils.gutendex_api import get_featured_books, get_books_by_genres, get_book_details
from utils.story_generator import generate_story


app = Flask(__name__)

# Ensure 'static/audio' directory exists
AUDIO_DIR = "static/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

def generate_audio_from_text(book_id, text_url):
    """
    Fetch the plain text version of the book and convert it to an MP3 file.
    """
    try:
        response = requests.get(text_url)
        response.raise_for_status()
        book_text = response.text[:5000]  # Limit text to first 5000 characters

        # Convert text to speech
        tts = gTTS(book_text, lang="en")
        audio_path = os.path.join(AUDIO_DIR, f"book_{book_id}.mp3")
        tts.save(audio_path)
        
        return audio_path
    except Exception as e:
        print("Error generating audiobook:", e)
        return None

# ---------------- ROUTES ---------------- #
@app.route("/")
def home():
    books = get_featured_books()
    return render_template("home.html", books=books)

@app.route("/by_genres")
def by_genres():
    genres = get_books_by_genres()
    return render_template("by_genres.html", genres=genres)

@app.route("/book/<int:book_id>")
def book_detail(book_id):
    book, text_url = get_book_details(book_id)
    return render_template("book.html", book=book, text_url=text_url)

@app.route("/audiobooks")
def audiobooks():
    books = get_books_by_genres()["Fiction"]["Adventure"]  # Use adventure books for audiobooks
    return render_template("audiobooks.html", books=books)

@app.route("/audiobook/<int:book_id>")
def audiobook_detail(book_id):
    book, text_url = get_book_details(book_id)
    if not book or not text_url:
        return render_template("error.html", message="Book not found"), 404

    audio_path = generate_audio_from_text(book_id, text_url)
    
    return render_template("audiobook_detail.html", book=book, audio_path=url_for('static', filename=f'audio/book_{book_id}.mp3'))

@app.route("/generate_story")
def generate_story_page():
    return render_template("generate_story.html")

# ---------------- STORY GENERATION API (Using GPT-Neo) ---------------- #
@app.route("/generate_story_api", methods=['POST'])
def generate_story_api():
    """
    API endpoint to generate a story using GPT-Neo.
    """
    data = request.get_json()
    prompt = data.get("prompt", "").strip()
    age_group = data.get("age_group", "8-10")  # Default to 8-10 if not provided

    if not prompt:
        return jsonify({"error": "Story prompt is required!"}), 400

    story = generate_story(prompt, age_group)  # Use GPT-Neo model to generate the story
    return jsonify({"story": story})

if __name__ == "__main__":
    app.run(debug=True)
