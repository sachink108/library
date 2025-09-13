import streamlit
from agentic_library.schema import Book

def show_sidebar(st:streamlit, books:list[Book])-> tuple[str, str]:
    st.sidebar.title("Filters")

    authors = sorted(set(book.author for book in books if book.author))  # book.author is author
    selected_author = st.sidebar.selectbox(
        "Filter by Author",
        ["All"] + authors
    )
    categories = sorted(set(book.genre for book in books if book.genre))  # book.genre is genre/category
    selected_category = st.sidebar.selectbox(
        "Filter by Category", 
        ["All"] + categories
    )
    return selected_author, selected_category
