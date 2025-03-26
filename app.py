import requests
from flask import Flask, render_template, request, jsonify
from flask_caching import Cache
from utils.gutendex_api import get_featured_books, get_books_by_genres, get_book_details
from utils.librivox_api import get_audiobooks
from utils.story_generator import generate_story

# Initialize Flask app
app = Flask(__name__)

# Initialize caching
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# ----------- ROUTES -----------

@app.route("/")
def home():
    """Load the homepage with featured books."""
    featured_books = get_featured_books()
    return render_template("home.html", books=featured_books)

@app.route("/by_genres")
def by_genres():
    """Load the genres page with categorized books."""
    genres = get_books_by_genres()
    return render_template("by_genres.html", genres=genres)

@app.route("/book/<int:book_id>")
def book_detail(book_id):
    """Load book details and display in an iframe or plain text."""
    book, text_url = get_book_details(book_id)
    return render_template("book.html", book=book, text_url=text_url)

@app.route("/audiobooks")
def audiobooks():
    """Fetch children's audiobooks from Librivox API."""
    genres = get_audiobooks()
    return render_template("audiobooks.html", genres=genres)

@app.route("/audiobook/<int:book_id>")
def audiobook_detail(book_id):
    """Fetch a single audiobook's details from Librivox API."""
    book = get_audiobooks(book_id=book_id)
    return render_template("audiobook_detail.html", book=book)

@app.route("/generate_story")
def generate_story_page():
    """Render the AI story generator page."""
    return render_template("generate_story.html")

@app.route("/generate_story_api", methods=["POST"])
def generate_story_api():
    """Generate a story based on user input."""
    data = request.get_json()
    prompt = data.get("prompt", "a curious adventurer")
    story = generate_story(prompt)
    return jsonify({"story": story})

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
