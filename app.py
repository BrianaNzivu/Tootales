import os
import requests
from flask import Flask, render_template, url_for, request, jsonify
from utils.gutendex_api import get_featured_books, get_books_by_genres, get_book_details
from utils.story_generator import generate_story  # Our GPT-Neo story generator
from utils.audiobook_generator import get_all_audiobooks, get_audiobook_by_id  # Importing Firestore functions

app = Flask(__name__)

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
    books = get_all_audiobooks()  # Fetch all audiobooks from Firestore
    return render_template("audiobooks.html", books=books)

@app.route("/audiobook/<book_id>")
def audiobook_detail(book_id):
    book = get_audiobook_by_id(book_id)
    if not book:
        return render_template("error.html", message="Book not found"), 404

    # Map Firestore field to the one your HTML expects
    book['cover_url'] = book.get('cover_image_url')  

    audio_url = book.get("audio_url")
    return render_template("audiobook_detail.html", book=book, audio_url=audio_url)

@app.route("/generate_story")
def generate_story_page():
    return render_template("generate_story.html")

@app.route("/generate_story_api", methods=["POST"])
def generate_story_api():
    data = request.get_json()
    prompt = data.get("prompt", "").strip()
    age_group = data.get("age_group", "8-10")  # Default to 8-10 if not provided

    if not prompt:
        return jsonify({"error": "Story prompt is required!"}), 400

    story = generate_story(prompt, age_group)
    return jsonify({"story": story})


if __name__ == "__main__":
    app.run(debug=True)
