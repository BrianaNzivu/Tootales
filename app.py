import requests
from flask import Flask, render_template

app = Flask(__name__)

def fetch_books_gutendex(search_query, rows=8, page=1):
    """
    Fetch books from the Gutendex API by search query,
    filtering for English language.
    """
    base_url = "https://gutendex.com/books"
    params = {
        "languages": "en",
        "search": search_query,
        "page": page
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        books = data.get("results", [])
        return books[:rows]
    except Exception as e:
        print("Error fetching books:", e)
        return []

@app.route("/")
def home():
    # Define categories with search queries tailored for fun, engaging children’s books.
    category_queries = {
        "Picture Books": "picture book",
        "Fairy Tales": "fairy tale",
        "Chapter Books": "chapter book",
        "Kids Poems": "children poetry",
        "Comic Books": "comic",
        "Phonics Books": "phonics"
    }
    categories = {}
    for category, query in category_queries.items():
        categories[category] = fetch_books_gutendex(query, rows=8, page=1)
    return render_template("home.html", categories=categories)

@app.route("/book/<int:book_id>")
def book_detail(book_id):
    """
    Fetches the book details from Gutendex API by its id.
    Checks for an HTML version of the text; if not found, falls back to plain text.
    """
    url = f"https://gutendex.com/books/{book_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        book = response.json()
    except Exception as e:
        print("Error fetching book details:", e)
        book = None

    text_url = None
    if book:
        formats = book.get("formats", {})
        # Prefer HTML version, else plain text
        for key, value in formats.items():
            if "text/html" in key and value.endswith(".htm"):
                text_url = value
                break
        if not text_url:
            for key, value in formats.items():
                if "text/plain" in key and value.endswith(".txt"):
                    text_url = value
                    break
    return render_template("book.html", book=book, text_url=text_url)

if __name__ == "__main__":
    app.run(debug=True)
