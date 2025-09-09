import sqlite3
import uuid
import base64

# Initialize database
DB_PATH = "books_collection.db"
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE,
            title TEXT,
            author TEXT,
            tagline TEXT,
            genre TEXT,
            image_b64 TEXT,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

def save_book_to_db(book:dict):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO books (uuid, title, author, tagline, genre, image_b64) VALUES (?, ?, ?, ?, ?, ?)",
                (str(uuid.uuid4()),
                book.get("title", ""), 
                book.get("author", ""), 
                book.get("tagline", ""),
                book.get("genre", ""),
                book.get("image", ""))
        )
        conn.commit()

def get_books_from_db():
    books = []
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT title, author, tagline, genre, image_b64 FROM books")
        books = c.fetchall()    
    return books


def delete_book_from_db(book_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
