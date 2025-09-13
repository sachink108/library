import sqlite3
import uuid
from agentic_library.schema import Book

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

def save_book_to_db(book:Book)  -> None:
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO books (uuid, title, author, tagline, genre, image_b64) VALUES (?, ?, ?, ?, ?, ?)",
                (str(uuid.uuid4()),
                book.title,
                book.author,
                book.tagline,
                book.genre,
                book.image)
        )
        conn.commit()

def get_books_from_db() -> list[Book]:
    books = []
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT uuid, title, author, tagline, genre, image_b64 FROM books")
        books = c.fetchall()
        # print(books)
        books = [Book(uuid=row[0], title=row[1], author=row[2], 
                tagline=row[3], genre=row[4], image=row[5]) for row in books]

    return books

def delete_book_from_db(book_id) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM books WHERE uuid = ?", (book_id,))
        conn.commit()

def update_book(book_id, title, author, tagline, genre) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            UPDATE books 
            SET title = ?, author = ?, tagline = ?, genre = ?
            WHERE uuid = ?
        """, (title, author, tagline, genre, book_id))
        conn.commit()