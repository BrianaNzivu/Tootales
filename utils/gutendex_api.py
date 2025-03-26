import requests

BASE_URL = "https://gutendex.com/books"

def fetch_books_gutendex(search_query, rows=8, page=1):
    """Fetch books from the Gutendex API filtered for English."""
    params = {
        "languages": "en",
        "search": search_query,
        "page": page
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json().get("results", [])[:rows]
    except Exception as e:
        print("Error fetching books:", e)
        return []

def get_featured_books():
    """Fetch featured children's books."""
    return fetch_books_gutendex("children's literature", rows=8, page=1)

def get_books_by_genres():
    """Fetch categorized books."""
    genres = {
        "Fiction": {
            "Adventure": "adventure fiction",
            "Fantasy": "fantasy fiction",
        },
        "Non-Fiction": {
            "Biography": "biography",
            "Self-Help": "self help",
        }
    }
    return {genre: {sub: fetch_books_gutendex(query) for sub, query in subgenres.items()} for genre, subgenres in genres.items()}

def get_book_details(book_id):
    """Fetch a single book's details from Gutendex API."""
    url = f"{BASE_URL}/{book_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        book = response.json()
        text_url = next((value for key, value in book.get("formats", {}).items() if "text/html" in key or "text/plain" in key), None)
        return book, text_url
    except Exception as e:
        print("Error fetching book details:", e)
        return None, None
