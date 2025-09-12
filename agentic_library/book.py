import os
import streamlit as st
from agentic_library.db import save_book_to_db, get_books_from_db
from agentic_library.book_agent import identify_book_details


@st.dialog("Add a Book")
def add_book():
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
                st.write("Identified Book Details:")
                st.write(f"**Title:** {book['title']}")
                st.write(f"**Author:** {book['author']}")
                st.write(f"**Tagline:** {book['tagline']}")
                st.write(f"**Genre:** {book['genre']}")
                # st.json(book)
                save_book_to_db(book)
            except Exception as e:
                st.error(f"Error identifying book: {e}")
        os.remove(temp_path)
