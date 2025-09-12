import re
import openai
import base64
from dotenv import load_dotenv
import streamlit as st
import sqlite3
import json
import os

load_dotenv()
# Set your OpenAI API key
client = openai.OpenAI()  # Create a client instance

def read_image_file(image_path):
    with open(image_path, "rb") as f:
        return f.read()

def identify_book_details_mock(image_path):
    return {'author': 'John Grisham', 'title': 'A Time for Mercy', 'tagline': 'Can a killer ever be above the law?'}

def identify_book_details(image_path):
    image_bytes = read_image_file(image_path)
    image_b64 = base64.b64encode(image_bytes).decode()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            # {"role": "system", "content": "You are a helpful assistant that identifies books from cover images. Always respond in JSON format with the following fields: 'author', 'title', 'tagline', and 'image' (base64-encoded image string)."},
            {"role": "user", "content": [
                {"type": "text", "text": "Identify the book title, author, and any other details from this cover image. Respond only with a JSON object containing 'author', 'title', 'tagline', and 'image' (base64-encoded image string)."},
                {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + image_b64}}
            ]}
        ],
        max_tokens=400
    )
    details = response.choices[0].message.content
    json_block = re.search(r"```json(.*?)```", details, re.S) 
    return json.loads(json_block.group(1).strip())

# Initialize database
DB_PATH = "books_collection.db"
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            tagline TEXT,
            image_b64 TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def save_book_to_db(title, author, tagline, image_b64):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO books (title, author, tagline, image_b64) VALUES (?, ?, ?, ?)",
        (title, author, tagline, image_b64)
    )
    conn.commit()
    conn.close()

def get_books_from_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT title, author, tagline, image_b64 FROM books")
    books = c.fetchall()
    conn.close()
    return books

# Streamlit UI
st.title("Book Collection Builder")

uploaded_file = st.file_uploader("Upload a book cover image", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image_bytes = uploaded_file.read()
    temp_path = "temp_uploaded_image.jpg"
    with open(temp_path, "wb") as f:
        f.write(image_bytes)
    with st.spinner("Identifying book details..."):
        try:
            #details = identify_book_details(temp_path)
            details_json = identify_book_details_mock(temp_path)
            st.success("Book identified!")
            st.json(details_json)
            save_book_to_db(
                details_json.get("title", ""),
                details_json.get("author", ""),
                details_json.get("tagline", ""),
                details_json.get("image", "")
            )
        except Exception as e:
            st.error(f"Error identifying book: {e}")
    os.remove(temp_path)

st.header("Your Book Collection")
books = get_books_from_db()
for title, author, tagline, image_b64 in books:
    st.subheader(title)
    st.write(f"**Author:** {author}")
    st.write(f"**Tagline:** {tagline}")
    if image_b64:
        st.image(base64.b64decode(image_b64), use_column_width=True)
    st.markdown("---")



# if __name__ == "__main__":
#     if len(sys.argv) > 1 and sys.argv[1] == "run":
#         subprocess.run(["streamlit", "run", __file__])
    # image_path = "./20250902_085524.jpg"
    # details = identify_book_details(image_path)
    # print(details)