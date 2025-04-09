import requests

GUTENDEX_API = "https://gutendex.com/books"

def fetch_books_gutendex(search_query, rows=50, page=1):
    params = {
        "languages": "en",
        "search": search_query,
        "page": page
    }
    try:
        response = requests.get(GUTENDEX_API, params=params)
        response.raise_for_status()
        data = response.json()
        books = data.get("results", [])
        return books[:rows]
    except Exception as e:
        print("Error fetching books:", e)
        return []

def get_featured_books():
    return fetch_books_gutendex("children's literature", rows=8, page=1)

def get_books_by_genres():
    genres = {
        "Fiction": {
            "Adventure": fetch_books_gutendex("adventure fiction"),
            "Fantasy": fetch_books_gutendex("fantasy fiction"),
        },
        "Non-Fiction": {
            "Biography": fetch_books_gutendex("biography"),
            "History": fetch_books_gutendex("history non-fiction"),
        }
    }
    return genres

def get_book_details(book_id):
    url = f"https://gutendex.com/books/{book_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        book = response.json()
        text_url = None

        formats = book.get("formats", {})
        for key, value in formats.items():
            if "text/plain" in key:
                text_url = value
                break

        return book, text_url
    except Exception as e:
        print("Error fetching book details:", e)
        return None, None