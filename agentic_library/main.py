import base64
import streamlit as st
from PIL import Image
import io

from agentic_library.db import get_books_from_db
from agentic_library.book import add_book

if st.button("Log in with Google"):
    st.login()
# st.login()

# --- Login Screen ---
def login_screen():
    st.header("This app is private")
    st.subheader("Please login with your Google account to continue.")
    st.button("Login with Google", on_click=st.login)
    
if not st.user.is_logged_in:
    login_screen()
else:
    st.user.name, st.user.email

# def login_regular():
#     st.title("Login")
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")
#     if st.button("Login"):
#         # Simple hardcoded authentication for demo purposes
#         if username == "admin" and password == "password":
#             st.session_state.logged_in = True
#             st.success("Logged in successfully!")
#             # st.experimental_rerun()
#         else:
#             st.error("Invalid username or password.")

# if not st.session_state.logged_in:
#     login_regular()
#     st.stop()
# Streamlit UI
st.markdown("""
        <style>
            .block-container {
                padding-top: 1rem; /* Adjust this value as needed, 0rem for minimal top space */
                padding-bottom: 0rem;
                padding-left: 5rem;
                padding-right: 5rem;
            }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(
    layout="wide",
    page_title="My Streamlit App",
    page_icon=":books:"
)
st.title("My Library")

# --- Sidebar for categories ---
books = get_books_from_db()
# authors = sorted(set(book[1] for book in books if book[1]))  # book[1] is author
# selected_author = st.sidebar.selectbox(
#     "Filter by Author",
#     ["All"] + authors
# )
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

cols = st.columns(4)
for idx, (title, author, tagline, genre, image_b64) in enumerate(books):
    with cols[idx % 4]:
        st.subheader(title)
        # st.write(f"**Author:** {author}")
        # st.write(f"**Tagline:** {tagline}")
        # st.write(f"**Genre:** {genre}")
        if image_b64:
            image_data = base64.b64decode(image_b64)
            image = Image.open(io.BytesIO(image_data))
            image.thumbnail((200, 300))
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            st.image(buf.getvalue(), width='content')
            
        # st.markdown("---")

