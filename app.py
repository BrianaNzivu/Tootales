import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from flask import Flask, render_template, url_for, request, jsonify, session, redirect
from utils.gutendex_api import get_featured_books, get_books_by_genres, get_book_details
from utils.audiobook_generator import get_all_audiobooks, get_audiobook_by_id
from utils.story_generator import generate_story
from functools import wraps
from datetime import timedelta
from flask import Flask, request, jsonify, render_template, url_for
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.permanent_session_lifetime = timedelta(minutes=30)  
try:
    model_name = "EleutherAI/gpt-neo-125M"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    story_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {str(e)}")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_name"):
            return redirect(url_for("auth_bp.login"))
        return f(*args, **kwargs)
    return decorated_function

from auth import auth_bp  
app.register_blueprint(auth_bp, url_prefix="/auth")

# ---------------- ROUTES ---------------- #

@app.route("/")
def root_redirect():
    if session.get("user_name"):
        return redirect(url_for("home"))
    return redirect(url_for("auth_bp.login"))

@app.route("/by_genres")
@login_required
def by_genres():
    genres = get_books_by_genres()
    return render_template("by_genres.html", genres=genres, user_name=session.get("user_name"))

@app.route("/book/<int:book_id>")
def book_detail(book_id):
    book, text_url = get_book_details(book_id)

    if not book.get("cover_url"):
        book["cover_url"] = url_for("static", filename="assets/fallback.jpg")

    return render_template("book.html", book=book, text_url=text_url)

@app.route("/home")
@login_required
def home():
    books = get_featured_books()
    return render_template("home.html", books=books, user_name=session.get("user_name"))

@app.route("/audiobooks")
@login_required
def audiobooks():
    books = get_all_audiobooks()  
    return render_template("audiobooks.html", books=books, user_name=session.get("user_name"))

@app.route("/audiobook/<book_id>")
@login_required
def audiobook_detail(book_id):
    book = get_audiobook_by_id(book_id)
    if not book:
        return render_template("error.html", message="Book not found"), 404
    book['cover_url'] = book.get('cover_image_url')
    return render_template("audiobook_detail.html", book=book, audio_url=book.get("audio_url"), user_name=session.get("user_name"))

@app.route("/fabric")
@login_required
def fabric():
    return render_template("fabric.html", user_name=session.get("user_name"))

@app.route("/generate_story")
@login_required
def generate_story_page():
    return render_template("generate_story.html", user_name=session.get("user_name"))
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", message="Page not found"), 404

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/api/generate-story', methods=['POST'])
def api_generate_story():
    data = request.get_json()
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    
    try:
        story = generate_story(prompt)
        story_text = story.replace(prompt, '').strip()
        return jsonify({'story': story_text})
    except Exception as e:
        app.logger.error(f"Error generating story: {str(e)}")
        return jsonify({'error': 'Failed to generate story'}), 500