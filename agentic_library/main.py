"""
Main Streamlit application for the Agentic Library.
This script sets up the user interface for a personal library management app, allowing users to log in, view, add, edit, delete, and search for books. 
It integrates with custom modules for book management, user authentication, sidebar filters, and database operations.
Features:
- Custom page styling and configuration.
- User authentication and session management.
- Sidebar with author and genre filters.
- Top bar for adding new books and searching.
- Dynamic display of books with options to view details, edit, or delete.
- Integration with a database for persistent storage of books and users.
Modules imported:
- `agentic_library.book`: Functions for book operations (add, delete, edit, display).
- `agentic_library.sidebar`: Sidebar filter UI.
- `agentic_library.db`: Database operations for books and users.
- `agentic_library.login`: Custom login screen.
Usage:
Run this script with Streamlit to launch the Agentic Library web app.
Install: poetry install
Run: poetry run streamlit run agentic_library/main.py
"""

import streamlit as st

from agentic_library.book import add_book, delete_book, display_book_details, edit_book_details, display_book_image
from agentic_library.sidebar import show_sidebar
from agentic_library.db import get_books_from_db
from agentic_library.db import get_user_by_email, add_user_to_db
from agentic_library.login import centered_login_screen

    
# Streamlit UI
st.markdown("""
        <style>
            .block-container {
                padding-top: 1rem; /* Adjust this value as needed, 0rem for minimal top space */
                padding-bottom: 0rem;
                padding-left: 3rem;
                padding-right: 3rem;
            }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(
    layout="wide",
    page_title="My Streamlit App",
    page_icon=":books:",
    initial_sidebar_state="auto",
    
    menu_items={
        'Report a bug': "mailto:sachink108@gmail.com",
        'About': "# This is your personal library and an *extremely* cool app!"
    }
)

# Add a background image to the top of the page
if not st.user.is_logged_in:
    centered_login_screen()
    st.stop()
else:
    st.title("My Library")
    st.sidebar.write(f"Welcome, {getattr(st.user, 'display_name', st.user.name)}!")
    if st.sidebar.button("Logout", type="secondary", use_container_width=False, key="logout_sidebar", help="Logout", icon="🚪"):
        st.logout()
    add_user_to_db(st.user)

books = get_books_from_db(get_user_by_email(st.user.email)['user_id'])

# Top bar with Add Book and Search
col1, col2, col3 = st.columns([0.6, 1, 2])
with col1:
    if st.button("➕ Add a new book", key="add_book_top"):
        user_id = get_user_by_email(st.user.email)['user_id']
        add_book(user_id=user_id)
with col2:
    search_query = st.text_input("🔍 Search for books by title, author, or genre", "", 
                                label_visibility="collapsed", 
                                key="search_top",
                                placeholder="Search books...",
                                help="Type to search books by title, author, or genre")
    if search_query:
        books = [book for book in books if
                    search_query.lower() in book.title.lower() or
                    search_query.lower() in book.author.lower() or
                    search_query.lower() in book.genre.lower()]
with col3:    
    if st.button("Clear Search", key="clear_search_top", icon="❌", 
                on_click=lambda: st.session_state.update({"search_top": ""}), 
                help="Clear search input"):
        books = get_books_from_db(get_user_by_email(st.user.email)['user_id'])


# --- Sidebar for Filters ---
selected_author, selected_category = show_sidebar(st, books)

# Display books
if selected_author != "All":
    books = [book for book in books if book.author == selected_author]
if selected_category != "All":
    books = [book for book in books if book.genre == selected_category]

cols = st.columns(6, border=True)
for idx, book in enumerate(books):
    with cols[idx % 6]:
        view_col, edit_col, delete_col = st.columns(3)
        with st.container():
            if view_col.button("👁️", key=f"view_btn_{idx}", help="View details", use_container_width=True):
                display_book_details(book)
            if edit_col.button("✏️", key=f"edit_btn_{idx}", help="Edit book", use_container_width=True):
                edit_book_details(book)
            if delete_col.button("🗑️", key=f"delete_btn_{idx}", help="Delete book"):
                delete_book(book)
            display_book_image(book)


