import requests
from flask import url_for

LIBRIVOX_API = "https://librivox.org/api/feed/audiobooks/"

def fetch_librivox_audiobooks(limit=30):
    """
    Fetch a list of children's audiobooks from Librivox API.
    """
    params = {
        "format": "json",
        "genre": "children",  # Use genre instead of subject
        "limit": limit
    }
    try:
        response = requests.get(LIBRIVOX_API, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("books", [])
    except Exception as e:
        print("Error fetching audiobooks:", e)
        return []

def get_audiobook_details(book_id):
    """
    Fetch details for a single audiobook, including cover and playable MP3.
    """
    url = f"{LIBRIVOX_API}?id={book_id}&format=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        books = response.json().get("books", [])
        if not books:
            print("No book found for ID:", book_id)
            return None  # Ensure None is returned when no book exists

        book = books[0]  # Take first result
        authors = book.get("authors", [])
        author_name = f"{authors[0]['first_name']} {authors[0]['last_name']}" if authors else "Unknown"

        # ✅ Ensure we get a valid cover image
        cover_url = book.get("url_thumb", url_for('static', filename='assets/fallback.jpg', _external=True))

        # ✅ Extract the first MP3 file if available
        audio_url = None
        zip_url = book.get("url_zip_file")
        if zip_url:
            audio_url = zip_url.replace(".zip", "_01_64kb.mp3")  # Convert ZIP URL to MP3

        return {
            "id": book.get("id"),
            "title": book.get("title"),
            "description": book.get("description", "No description available."),
            "audio_url": audio_url,  # Direct MP3 file
            "cover_url": cover_url,
            "author": author_name
        }
    except Exception as e:
        print("Error fetching audiobook details:", e)
        return None  # Ensure None is returned if an error occurs
