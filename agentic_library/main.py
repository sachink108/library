import os
import base64
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import io

from agentic_library.db import save_book_to_db, get_books_from_db
from agentic_library.book_agent import identify_book_details
from agentic_library.book import add_book

# Streamlit UI
st.title("My Library")

# --- Sidebar for categories ---
books = get_books_from_db()
authors = sorted(set(book[1] for book in books if book[1]))  # book[1] is author
selected_author = st.sidebar.selectbox(
    "Filter by Author",
    ["All"] + authors
)
books = get_books_from_db()
categories = sorted(set(book[3] for book in books if book[3]))  # book[3] is genre/category
selected_category = st.sidebar.selectbox(
    "Filter by Category", 
    ["All"] + categories
)

# --- Upload button and uploader ---
if st.button("Add a Book"):
    st.info("Please upload a book cover image below.")
    add_book()

st.header("Your Book Collection")

# Display books
books = get_books_from_db()
if selected_category != "All":
    books = [book for book in books if book[3] == selected_category]

for title, author, tagline, genre, image_b64 in books:
    st.subheader(title)
    st.write(f"**Author:** {author}")
    st.write(f"**Tagline:** {tagline}")
    st.write(f"**Genre:** {genre}")
    # Resize the image before displaying

    if image_b64:
        image_data = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(image_data))
        image.thumbnail((200, 300))  # Set max width and height
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        st.image(buf.getvalue(), width='content')
    st.markdown("---")

