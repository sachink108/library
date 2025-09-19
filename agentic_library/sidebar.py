import streamlit
from agentic_library.schema import Book

def show_sidebar(st:streamlit, books:list[Book])-> tuple[str, str]:
    """
    Displays sidebar filters for authors and categories using Streamlit.
    Args:
        st (streamlit): The Streamlit module or object used to render UI components.
        books (list[Book]): A list of Book objects to extract authors and categories from.
    Returns:
        tuple[str, str]: A tuple containing the selected author and selected category from the sidebar filters.
    """
    
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
