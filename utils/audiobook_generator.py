import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate('firebase_key.json')
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

def get_all_audiobooks():
    try:
        books_ref = db.collection('audiobooks')
        docs = books_ref.stream()

        books = []
        for doc in docs:
            book = doc.to_dict()
            book['id'] = doc.id  # Include the document ID for each book
            book['cover_url'] = doc.get('cover_image_url')  # Fetch cover_image_url from Firestore
            books.append(book)

        return books
    except Exception as e:
        print(f"Error fetching audiobooks: {e}")
        return []

    
def get_audiobook_by_id(book_id):
    try:
        # Fetch a single book document by its ID
        book_ref = db.collection('audiobooks').document(book_id)
        book_doc = book_ref.get()

        if book_doc.exists:
            return book_doc.to_dict()  # Return the book details as a dictionary
        else:
            return None  # Book not found
    except Exception as e:
        print(f"Error fetching audiobook by ID {book_id}: {e}")
        return None
