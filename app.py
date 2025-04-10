import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, url_for, request, jsonify, session, redirect
from utils.gutendex_api import get_featured_books, get_books_by_genres, get_book_details
from utils.story_generator import generate_story
from utils.audiobook_generator import get_all_audiobooks, get_audiobook_by_id
from functools import wraps
from datetime import timedelta

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.permanent_session_lifetime = timedelta(minutes=30)  # Session timeout

# Define a login_required decorator for protected routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_name"):
            return redirect(url_for("auth_bp.login"))
        return f(*args, **kwargs)
    return decorated_function

# Register the authentication blueprint
from auth import auth_bp  # Ensure auth.py defines a Blueprint named auth_bp
app.register_blueprint(auth_bp, url_prefix="/auth")

# ---------------- ROUTES ---------------- #

@app.route("/")
def root_redirect():
    # Redirect authenticated users to home, otherwise to login
    if session.get("user_name"):
        return redirect(url_for("home"))
    return redirect(url_for("auth_bp.login"))

@app.route("/by_genres")
@login_required
def by_genres():
    genres = get_books_by_genres()
    return render_template("by_genres.html", genres=genres)

@app.route("/book/<int:book_id>")
def book_detail(book_id):
    book, text_url = get_book_details(book_id)
    return render_template("book.html", book=book, text_url=text_url)

@app.route("/home")
@login_required
def home():
    books = get_featured_books()
    return render_template("home.html", books=books, user_name=session.get("user_name"))

@app.route("/audiobooks")
@login_required
def audiobooks():
    books = get_all_audiobooks()  # Fetch all audiobook documents from Firestore
    return render_template("audiobooks.html", books=books, user_name=session.get("user_name"))

@app.route("/audiobook/<book_id>")
@login_required
def audiobook_detail(book_id):
    book = get_audiobook_by_id(book_id)
    if not book:
        return render_template("error.html", message="Book not found"), 404
    # Map Firestore field 'cover_image_url' to template variable 'cover_url'
    book['cover_url'] = book.get('cover_image_url')
    return render_template("audiobook_detail.html", book=book, audio_url=book.get("audio_url"), user_name=session.get("user_name"))

@app.route("/fabric")
def fabric():
    return render_template("fabric.html", user_name=session.get("user_name"))

@app.route("/generate_story")
@login_required
def generate_story_page():
    return render_template("generate_story.html", user_name=session.get("user_name"))

@app.route("/generate_story_api", methods=["POST"])
@login_required
def generate_story_api():
    data = request.get_json()
    prompt = data.get("prompt", "").strip()
    age_group = data.get("age_group", "8-10")  # Default to 8-10 if not provided

    # Validate input
    if not prompt:
        return jsonify({"error": "Story prompt is required!"}), 400

    valid_age_groups = ["8-10", "11-13", "14-16"]
    if age_group not in valid_age_groups:
        return jsonify({"error": "Invalid age group!"}), 400

    story = generate_story(prompt, age_group)
    return jsonify({"story": story})

# Global error handler for 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", message="Page not found"), 404

if __name__ == "__main__":
    app.run(debug=True)