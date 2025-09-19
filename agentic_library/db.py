import streamlit as st
import sqlite3
import uuid
from agentic_library.schema import Book

# Initialize database
DB_PATH = "library.db"
def init_db():
    """
    Initialize the SQLite database and create tables for users and books if they do not exist.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT UNIQUE,
            first_name TEXT,
            last_name TEXT,
            email TEXT UNIQUE
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE,
            title TEXT,
            author TEXT,
            tagline TEXT,
            genre TEXT,
            image_b64 TEXT,
            user_id TEXT,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    """)
    conn.commit()
    conn.close()

init_db()


def get_user_by_email(email: str) -> dict | None:
    """
    Retrieve a user from the database by their email address.
    Returns a dictionary with user details or None if not found.
    """
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT user_id, first_name, last_name, email FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        if user:
            return {
                "user_id": user[0],
                "first_name": user[1],
                "last_name": user[2],
                "email": user[3]
            }
        return None

def add_user_to_db(user) -> None:
    """
    Add a new user to the database if they do not already exist.
    The user object should have email, given_name, and family_name attributes.
    """
    # --- Check if user exists in DB, if not add ---
    user_email = user.email
    _user = get_user_by_email(user_email)
    if not _user:
        first_name = user.given_name or ""
        last_name = user.family_name or ""
        print(f"Adding user to DB: {user_email}, {first_name}, {last_name}")
        # --- Add user to DB ---
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            user_id = str(uuid.uuid4())
            c.execute(
                "INSERT INTO users (first_name, last_name, email, user_id) VALUES (?, ?, ?, ?)",
                (first_name, last_name, user_email, user_id)
            )
            conn.commit()
        print("User added to DB {}".format(user_email))

def save_book_to_db(book: Book, user_id: str) -> None:
    """
    Save a Book object to the database for the given user_id.
    """
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO books (uuid, title, author, tagline, genre, image_b64, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (str(uuid.uuid4()),
                book.title,
                book.author,
                book.tagline,
                book.genre,
                book.image,
                user_id)
        )
        conn.commit()

@st.cache_data(show_spinner=False)
def get_books_from_db_cached(user_id: str) -> list[Book]:
    """
    Cached version of get_books_from_db for performance.
    Returns a list of Book objects for the given user_id.
    """
    return get_books_from_db(user_id)

def get_books_from_db(user_id: str) -> list[Book]:
    """
    Retrieve all books for a given user_id from the database.
    Returns a list of Book objects.
    """
    books = []
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT uuid, title, author, tagline, genre, image_b64 FROM books WHERE user_id = ?", (user_id,))
        books = c.fetchall()
        books = [Book(user_id=user_id, uuid=row[0], title=row[1], author=row[2], 
                tagline=row[3], genre=row[4], image=row[5]) for row in books]

    return books

def delete_book_from_db(book_id: str, user_id: str) -> None:
    """
    Delete a book from the database by its uuid and user_id.
    """
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM books WHERE uuid = ? AND user_id = ?", (book_id, user_id))
        conn.commit()

def update_book(book_id: str, title: str, author: str, tagline: str, genre: str, user_id: str) -> None:
    """
    Update the details of a book in the database for the given uuid and user_id.
    """
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            UPDATE books 
            SET title = ?, author = ?, tagline = ?, genre = ?
            WHERE uuid = ? AND user_id = ?
        """, (title, author, tagline, genre, book_id, user_id))
        conn.commit()