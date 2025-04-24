import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate('firebase_key.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def get_all_audiobooks():
    try:
        books_ref = db.collection('audiobooks')
        docs = books_ref.stream()

        books = []
        for doc in docs:
            book = doc.to_dict()
            book['id'] = doc.id 
            book['cover_url'] = doc.get('cover_image_url')  
            books.append(book)

        return books
    except Exception as e:
        print(f"Error fetching audiobooks: {e}")
        return []

    
def get_audiobook_by_id(book_id):
    try:

        book_ref = db.collection('audiobooks').document(book_id)
        book_doc = book_ref.get()

        if book_doc.exists:
            return book_doc.to_dict() 
        else:
            return None  # Book not found
    except Exception as e:
        print(f"Error fetching audiobook by ID {book_id}: {e}")
        return None
