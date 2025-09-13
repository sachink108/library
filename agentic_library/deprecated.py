st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=1500&q=80');
        background-size: cover;
        background-position: top center;
        background-repeat: no-repeat;
    }
    </style>
    """,
    unsafe_allow_html=True
)
"""
def add_book_expander():
    with st.expander("Add a Book", expanded=False):
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
                        accept = st.button("Accept Book", key="accept_book_exp", type="primary")
                    with col2:
                        reject = st.button("Reject Book", key="reject_book_exp")

                    if accept:
                        save_book_to_db(book)
                        st.success("Book saved to database!")
                        st.experimental_rerun()
                    elif reject:
                        st.info("Book addition cancelled.")
                        st.experimental_rerun()
                except Exception as e:
                    st.error(f"Error identifying book: {e}")
            os.remove(temp_path)

def display_book_details_expander(book: Book):
    with st.expander("Book Details", expanded=False):
        st.markdown(f"### {book.title}")
        st.markdown(f"**Author:** {book.author}")
        st.markdown(f"**Tagline:** {book.tagline}")
        st.markdown(f"**Genre:** {book.genre}")

        if book.image:
            image_data = base64.b64decode(book.image)
            image = Image.open(io.BytesIO(image_data))
            image.thumbnail((100, 200))
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            st.image(buf.getvalue(), width='content')

def edit_book_details_expander(book: Book):
    with st.expander("Edit Book Details", expanded=False):
        new_title = st.text_input("Title", value=book.title, key=f"title_{book.uuid}")
        new_author = st.text_input("Author", value=book.author, key=f"author_{book.uuid}")
        new_tagline = st.text_input("Tagline", value=book.tagline, key=f"tagline_{book.uuid}")
        new_genre = st.text_input("Genre", value=book.genre, key=f"genre_{book.uuid}")

        if st.button("Save Changes", key=f"save_{book.uuid}_exp", type="primary"):
            update_book(book.uuid, new_title, new_author, new_tagline, new_genre)
            st.success("Book details updated")
            st.experimental_rerun()

def delete_book_expander(book: Book, on_delete=None):
    with st.expander("Delete Book", expanded=False):
        st.markdown(f"Are you sure you want to delete **{book.title}** by **{book.author}**?")
        col1, col2 = st.columns(2)
        with col1:
            confirm = st.button("Delete", key=f"delete_{book.uuid}_exp", type="primary")
        with col2:
            cancel = st.button("Cancel", key=f"cancel_delete_{book.uuid}_exp")

        if confirm:
            delete_book_from_db(book.uuid)
            st.success("Book deleted successfully.")
            if on_delete:
                on_delete()
            st.experimental_rerun()
        elif cancel:
            st.info("Book deletion cancelled.")
            st.experimental_rerun()
"""
