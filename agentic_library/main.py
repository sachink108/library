import base64
import streamlit as st
from PIL import Image
import io

from agentic_library.book import add_book, delete_book, display_book_details, edit_book_details
from agentic_library.sidebar import show_sidebar
from agentic_library.db import get_books_from_db

if st.button("Log in with Google"):
    st.login()

# --- Login Screen ---
def login_screen():
    st.header("This app is private")
    st.subheader("Please login with your Google account to continue.")
    st.button("Login with Google", on_click=st.login)
    
if not st.user.is_logged_in:
    login_screen()
else:
    st.sidebar.write(f"Welcome, {st.user.name}!")

# Streamlit UI
st.markdown("""
        <style>
            .block-container {
                padding-top: 0rem; /* Adjust this value as needed, 0rem for minimal top space */
                padding-bottom: 0rem;
                padding-left: 3rem;
                padding-right: 3rem;
            }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(
    layout="wide",
    page_title="My Streamlit App",
    page_icon=":books:"
)

st.title("My Library")
if st.button("➕ Add a new book"):
    add_book()

# --- Sidebar for Filters ---
books = get_books_from_db()
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
            # delete_col = st.columns(1)[0]
            if view_col.button("👁️", key=f"view_btn_{idx}", help="View details"):
                display_book_details(book)
            if edit_col.button("✏️", key=f"edit_btn_{idx}", help="Edit book"):
                edit_book_details(book)
            if delete_col.button("🗑️", key=f"delete_btn_{idx}", help="Delete book"):
                delete_book(book)
                st.experimental_rerun()
        if book.image:
            image_data = base64.b64decode(book.image)
            image = Image.open(io.BytesIO(image_data))
            image.thumbnail((100, 200))
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            st.image(buf.getvalue(), width='content')

