import os
import streamlit as st
import base64
import uuid
import io
from PIL import Image
from agentic_library.db import save_book_to_db, update_book
from agentic_library.book_agent import identify_book_details
from agentic_library.schema import Book
from agentic_library.db import delete_book_from_db

def _process_image(temp_path):
    with st.spinner("Identifying book details...", show_time=True):
        try:
            book = identify_book_details(temp_path)
            st.success("Book identified!")                
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
                st.success("Book saved to database!")
            elif reject:
                st.info("Book addition cancelled.")
        except Exception as e:
            st.error(f"Error identifying book: {e}")
        os.remove(temp_path)

def _upload_book_cover():
    uploaded_file = st.file_uploader("Upload a book cover image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image_bytes = uploaded_file.read()
        temp_path = "temp_uploaded_image.jpg"
        with open(temp_path, "wb") as f:
            f.write(image_bytes)
        _process_image(temp_path)

def _manual_entry():
    title = st.text_input("Title")
    author = st.text_input("Author")
    tagline = st.text_input("Tagline")
    genre = st.text_input("Genre")
    image_file = st.file_uploader("Book cover image (optional)", type=["jpg", "jpeg", "png"])
    image_b64 = None
    if image_file is not None:
        image_bytes = image_file.read()
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    if st.button("Add Book", key="manual_add_book", type="primary"):
        if not title or not author:
            st.error("Title and Author are required.")
        else:
            book = Book(uuid=str(uuid.uuid4()),
                        title=title, 
                        author=author, 
                        tagline=tagline, 
                        genre=genre, 
                        image=image_b64)
            save_book_to_db(book)
            st.success("Book saved to database!")
            #st.stop()

def _take_a_photo():
    camera_photo = st.camera_input("Take a photo of the book cover")
    if camera_photo is not None:
        temp_path = "temp_camera_image.jpg"
        with open(temp_path, "wb") as f:
            f.write(camera_photo.getvalue())
        _process_image(temp_path)

@st.dialog("Add a Book")
def add_book()-> None:
    option = st.radio(
        "Choose how to add a book:",
        ["Take a photo", "Upload a photo", "Enter manually"],
        horizontal=True,
        help="You can either take a photo of the book cover, upload an image, or enter the details manually."
    )
    if option == "Take a photo":
        _take_a_photo()
    elif option == "Upload a photo":
        _upload_book_cover()
    elif option == "Enter manually":
        _manual_entry()
    
def display_book_image(book: Book):
    if book.image:
        image_data = base64.b64decode(book.image)
        image = Image.open(io.BytesIO(image_data))
        image.thumbnail((150, 300))
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        st.image(buf.getvalue(), width=150)

@st.dialog("Book Details")
def display_book_details(book: Book):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"### {book.title}")
        st.markdown(f"**Author:** {book.author}")
        st.markdown(f"**Tagline:** {book.tagline}")
        st.markdown(f"**Genre:** {book.genre}")

    with col2:
        display_book_image(book)

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