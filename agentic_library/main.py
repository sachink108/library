import os
import base64
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import io

from agentic_library.db import save_book_to_db, get_books_from_db
from agentic_library.book_agent import identify_book_details

# Streamlit UI
st.title("My Library")

# --- Sidebar for categories ---
books = get_books_from_db()
categories = sorted(set(book[3] for book in books if book[3]))  # book[3] is genre/category
selected_category = st.sidebar.selectbox(
    "Filter by Category", 
    ["All"] + categories
)
# --- Upload button and uploader ---
if st.button("Add a Book"):
    st.info("Please upload a book cover image below.")

    uploaded_file = st.file_uploader("Upload a book cover image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image_bytes = uploaded_file.read()
        temp_path = "temp_uploaded_image.jpg"
        with open(temp_path, "wb") as f:
            f.write(image_bytes)
        with st.spinner("Identifying book details...", show_time=True):
            try:
                book = identify_book_details(temp_path)
                st.success("Book identified!")
                st.json(book)
                save_book_to_db(book)
            except Exception as e:
                st.error(f"Error identifying book: {e}")
        os.remove(temp_path)

st.header("Your Book Collection")
books = get_books_from_db()

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

