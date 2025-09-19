"""
Module for managing book entries in the agentic_library application using Streamlit dialogs.
This module provides functions and dialogs for adding, editing, displaying, and deleting books.
Books can be added by uploading a cover image, taking a photo, or manual entry. The module
supports image cropping, book detail identification, and database operations.
Functions:
    _process_image(temp_path, user_id): Processes an uploaded or captured image to identify book details.
    _upload_book_cover(user_id): Handles uploading a book cover image and triggers processing.
    _manual_entry(user_id): Allows manual entry of book details, with optional cover image upload.
    _take_a_photo(user_id): Captures a photo using the camera, allows cropping, and processes the image.
    add_book(user_id): Streamlit dialog for adding a book via photo, upload, or manual entry.
    display_book_image(book): Displays the book's cover image in the UI.
    display_book_details(book): Streamlit dialog for displaying book details.
    edit_book_details(book): Streamlit dialog for editing book details.
    delete_book(book, on_delete): Streamlit dialog for confirming and deleting a book.
Note:
    All dialogs use Streamlit's dialog API for interactive UI components.
"""
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
import streamlit_cropper

def _process_image(temp_path, user_id: str):
    """
    Processes an uploaded or captured image to identify book details using 
    the book agent.
    Allows user to verify and update details before saving to the database.
    """
    with st.spinner("Identifying book details...", show_time=True):
        try:
            book = identify_book_details(temp_path, user_id=user_id)
            st.success("Book identified!")
            book.user_id = user_id
            st.markdown("### Please verify/update the details below:")             
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
                save_book_to_db(book, user_id=user_id)
                st.success("Book saved to database! Please refresh to see it.")
                st.stop()
            elif reject:
                st.info("Book addition cancelled.")
                st.stop()
        except Exception as e:
            st.error(f"Error identifying book: {e}")
        
        os.remove(temp_path)

def _upload_book_cover(user_id: str):
    """
    Handles uploading a book cover image and triggers processing for 
    book detail identification.
    """
    uploaded_file = st.file_uploader("Upload a book cover image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image_bytes = uploaded_file.read()
        temp_path = "temp_uploaded_image.jpg"
        with open(temp_path, "wb") as f:
            f.write(image_bytes)
        _process_image(temp_path, user_id)

def _manual_entry(user_id: str):
    """
    Allows manual entry of book details, with optional cover image upload.
    Saves the book to the database after validation.
    """
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
            print(user_id)
            book = Book(user_id=user_id,
                        uuid=str(uuid.uuid4()),
                        title=title, 
                        author=author, 
                        tagline=tagline, 
                        genre=genre, 
                        image=image_b64)
            save_book_to_db(book, user_id=user_id)
            st.success("Book saved to database. Please refresh to see it.")
            st.stop()

def _take_a_photo(user_id: str):
    """
    Captures a photo using the camera, allows cropping, and processes the 
    image for book detail identification.
    """
    camera_photo = st.camera_input("Take a photo of the book cover")
    if camera_photo is not None:
        image = Image.open(camera_photo)
        st.markdown("**Crop and adjust the image before proceeding:**")
        cropped_img = streamlit_cropper.st_cropper(
            image,
            aspect_ratio=None,
            box_color='#FF4B4B',
            return_type='image',
            realtime_update=True,
            #min_container_width=300,
        )
        if cropped_img is not None:
            buf = io.BytesIO()
            cropped_img.save(buf, format="JPEG")
            temp_path = f"temp_camera_image_{user_id}.jpg"
            with open(temp_path, "wb") as f:
                f.write(buf.getvalue())
            _process_image(temp_path, user_id)
            st.stop()
    

@st.dialog("Add a Book")
def add_book(user_id: str) -> None:
    """
    Streamlit dialog for adding a book via photo, upload, or manual entry.
    Presents options and triggers the appropriate entry method.
    """
    option = st.radio(
        "Choose how to add a book:",
        ["Take a photo", "Upload a photo", "Enter manually"],
        horizontal=True,
        help="You can either take a photo of the book cover, upload an image, or enter the details manually."
    )
    if option == "Upload a photo":
        _upload_book_cover(user_id)
    elif option == "Take a photo":
        _take_a_photo(user_id)
    elif option == "Enter manually":
        _manual_entry(user_id)
    
def display_book_image(book: Book):
    """
    Displays the book's cover image in the UI, resizing for display.
    """
    if book.image:
        image_data = base64.b64decode(book.image)
        image = Image.open(io.BytesIO(image_data))
        image.thumbnail((150, 300))
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        st.image(buf.getvalue(), width=150)

@st.dialog("Book Details")
def display_book_details(book: Book):
    """
    Streamlit dialog for displaying book details including title, author, tagline, genre, and cover image.
    """
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
    """
    Streamlit dialog for editing book details. Allows user to update
    title, author, tagline, and genre.
    Saves changes to the database.
    """
    new_title = st.text_input("Title", value=book.title)
    new_author = st.text_input("Author", value=book.author)
    new_tagline = st.text_input("Tagline", value=book.tagline)
    new_genre = st.text_input("Genre", value=book.genre)

    if st.button("Save Changes", key=f"save_{book.uuid}", type="primary"):
        # Convert to named params for clarity
        update_book(
            book_id=book.uuid,
            user_id=book.user_id,
            title=new_title,
            author=new_author,
            tagline=new_tagline,
            genre=new_genre
        )
        st.success("Book details updated")

@st.dialog("Delete Book")
def delete_book(book: Book, on_delete=None):
    """
    Streamlit dialog for confirming and deleting a book from the database.
    Calls on_delete callback if provided.
    """
    st.markdown(f"Are you sure you want to delete **{book.title}** by **{book.author}**?")
    col1, col2 = st.columns(2)
    with col1:
        confirm = st.button("Delete", key=f"delete_{book.uuid}", type="primary")
    with col2:
        cancel = st.button("Cancel", key=f"cancel_delete_{book.uuid}")

    if confirm:
        delete_book_from_db(book.uuid, user_id=book.user_id)
        st.success("Book deleted successfully.")
        if on_delete:
            on_delete()
        st.stop()
    elif cancel:
        st.info("Book deletion cancelled.")
        st.stop()
