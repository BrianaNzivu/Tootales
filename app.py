import requests
from flask import Flask, render_template

app = Flask(__name__)

def fetch_books(genre="happy children's books", rows=8, page=1):
    """
    Fetches book metadata from the Internet Archive Advanced Search API
    based on the given genre (subject).
    """
    params = {
        "q": f"subject:\"{genre}\"",
        "fl[]": ["identifier", "title", "creator", "subject"],
        "rows": rows,
        "page": page,
        "output": "json"
    }
    url = "https://archive.org/advancedsearch.php"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        books = data.get("response", {}).get("docs", [])
        return books
    except Exception as e:
        print("Error fetching books:", e)
        return []

@app.route("/")
def home():
    # Define multiple categories with different subject queries
    category_queries = {
        "Picture Books": "Picture books for children",
        "Fairy Tales": "Fairy tales",
        "Chapter Books": '(subject:"juvenile fiction") AND (title:"chapter" OR subject:"chapter books")',
        "Kids Poems": "children's poetry",
        "Comic Books": '(subject:"comic books") AND (subject:"children" OR subject:"juvenile")',
        "Phonics Books": "phonics"
    }

    # For each category, fetch the books and store them in a dictionary
    categories = {}
    for category, query in category_queries.items():
        categories[category] = fetch_books(genre=query, rows=8, page=1)

    return render_template("home.html", categories=categories)

@app.route("/book/<identifier>")
def book_detail(identifier):
    """
    Embeds the Internet Archive's stream viewer for the chosen book identifier.
    """
    embed_url = f"https://archive.org/stream/{identifier}"
    return render_template("book.html", identifier=identifier, embed_url=embed_url)

if __name__ == "__main__":
    app.run(debug=True)
