import requests

LIBRIVOX_URL = "https://librivox.org/api/feed/audiobooks/"

def fetch_librivox_audiobooks(limit=30):
    """Fetch children's audiobooks from Librivox API."""
    params = {
        "format": "json",
        "subject": "children",
        "limit": limit
    }
    try:
        response = requests.get(LIBRIVOX_URL, params=params)
        response.raise_for_status()
        return response.json().get("books", [])
    except Exception as e:
        print("Error fetching audiobooks:", e)
        return []

def get_audiobooks(book_id=None):
    """Fetch all audiobooks or details of a single audiobook."""
    books = fetch_librivox_audiobooks()
    if book_id:
        return next((book for book in books if book["id"] == book_id), None)
    genres = {}
    for book in books:
        genre = book.get("genres", ["Other"])[0]
        genres.setdefault(genre, []).append(book)
    return genres
