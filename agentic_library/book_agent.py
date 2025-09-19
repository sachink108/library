"""
book_agent.py
-----------------
This module provides functions for identifying book details from cover images using OpenAI's vision models.
It includes utilities for reading image files, calling the OpenAI API, and returning structured book metadata.
Intended for use in the Streamlit personal library app.
"""
import re
import openai
import base64
import streamlit as st
import uuid
import json
from agentic_library.schema import Book


client = openai.OpenAI(api_key=st.secrets["OPENAPI"]["OPENAI_API_KEY"])  # Create a client instance

def read_image_file(image_path) -> bytes:
    """
    Reads an image file from the given path and returns its bytes.
    Args:
        image_path (str): Path to the image file.
    Returns:
        bytes: The image data in bytes.
    """
    with open(image_path, "rb") as f:
        return f.read()


def _call_openai_api(image_b64: str) -> str:
    """
    Calls the OpenAI API with a base64-encoded image to identify book details.
    Args:
        image_b64 (str): Base64-encoded image string.
    Returns:
        str: The response from the OpenAI API (expected to be a JSON string).
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", 
            "content": [
                {"type": "text", "text": "Identify the book title, author, genere, and any other details from this cover image. Respond only with a JSON object containing 'author', 'title', 'genre', 'tagline'."},
                {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + image_b64}}
            ]}
        ],
        max_tokens=200
    )
    return response.choices[0].message.content

def _call_openai_api_mock(image_b64: str) -> str:
    """
    Mock function to simulate OpenAI API response for testing purposes.
    Args:
        image_b64 (str): Base64-encoded image string.
    Returns:
        str: A mock JSON string with book details.
    """
    return """
    ```json
    {
        "author": "John Grisham",
        "title": "A Time for Mercy",
        "tagline": "Can a killer ever be above the law?",
        "genre": "Legal Thriller"
    }
    ```
    """

def identify_book_details(image_path, user_id: str) -> Book:
    """
    Identifies book details from a cover image using OpenAI's vision model.
    Args:
        image_path (str): Path to the image file.
        user_id (str): ID of the user adding the book.
    Returns:
        Book: A Book object populated with details extracted from the image.
    """
    image_bytes = read_image_file(image_path)
    image_b64 = base64.b64encode(image_bytes).decode()
    details = _call_openai_api(image_b64)
    # details = _call_openai_api_mock(image_b64)
    json_block = re.search(r"```json(.*?)```", details, re.S) 
    book_details = {}
    if json_block:
        book_details = json.loads(json_block.group(1).strip())
        book_details['user_id'] = user_id
        book_details['uuid'] = str(uuid.uuid4())
        book_details['image'] = image_b64

        return Book(**book_details)

    raise ValueError("No JSON block found in the response.")

