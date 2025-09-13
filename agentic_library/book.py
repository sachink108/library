import os
import streamlit as st
import base64
import io
from PIL import Image
from agentic_library.db import save_book_to_db, update_book
from agentic_library.book_agent import identify_book_details
from agentic_library.schema import Book
from agentic_library.db import delete_book_from_db



@st.dialog("Add a Book")
def add_book()-> None:
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
                # Make fields editable
                book.title = st.text_input("Title", value=book.title)
                book.author = st.text_input("Author", value=book.author)
                book.tagline = st.text_input("Tagline", value=book.tagline or "")
                book.genre = st.text_input("Genre", value=book.genre or "")

                col1, col2 = st.columns(2)
                with col1:
                    accept = st.button("Accept Book", key="accept_book",type="primary")
                with col2:
                    reject = st.button("Reject Book", key="reject_book")

                if accept:
                    save_book_to_db(book)
                    st.stop()
                    st.success("Book saved to database!")
                elif reject:
                    st.stop()
                    st.info("Book addition cancelled.")
            except Exception as e:
                st.error(f"Error identifying book: {e}")
        os.remove(temp_path)


@st.dialog("Book Details")
def display_book_details(book: Book):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"### {book.title}")
        st.markdown(f"**Author:** {book.author}")
        st.markdown(f"**Tagline:** {book.tagline}")
        st.markdown(f"**Genre:** {book.genre}")

    with col2:
        if book.image:
            image_data = base64.b64decode(book.image)
            image = Image.open(io.BytesIO(image_data))
            image.thumbnail((150, 300))
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            st.image(buf.getvalue(), width=150)

@st.dialog("Edit Book Details")
def edit_book_details(book: Book):
    new_title = st.text_input("Title", value=book.title)
    new_author = st.text_input("Author", value=book.author)
    new_tagline = st.text_input("Tagline", value=book.tagline)
    new_genre = st.text_input("Genre", value=book.genre)

    if st.button("Save Changes", key=f"save_{book.uuid}", type="primary"):
        update_book(book.uuid, new_title, new_author, new_tagline, new_genre)
        st.success("Book details updated")

@st.dialog("Delete Book")
def delete_book(book: Book, on_delete=None):
    st.markdown(f"Are you sure you want to delete **{book.title}** by **{book.author}**?")
    col1, col2 = st.columns(2)
    with col1:
        confirm = st.button("Delete", key=f"delete_{book.uuid}", type="primary")
    with col2:
        cancel = st.button("Cancel", key=f"cancel_delete_{book.uuid}")

    if confirm:
        delete_book_from_db(book.uuid)
        st.success("Book deleted successfully.")
        if on_delete:
            on_delete()
        st.stop()
    elif cancel:
        st.info("Book deletion cancelled.")
        st.stop()
