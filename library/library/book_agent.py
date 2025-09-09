import re
import openai
import base64
from dotenv import load_dotenv

import json


load_dotenv()
# Set your OpenAI API key
client = openai.OpenAI()  # Create a client instance

def read_image_file(image_path) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()

# def identify_book_details_mock(image_pat:str) -> dict:
#     return {'author': 'John Grisham', 'title': 'A Time for Mercy', 'tagline': 'Can a killer ever be above the law?',
#             'genre': 'Legal Thriller', 
#             'image': base64.b64encode(read_image_file(image_pat)).decode() }

def _call_openai_api(image_b64: str) -> str:
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

def identify_book_details(image_path):
    image_bytes = read_image_file(image_path)
    image_b64 = base64.b64encode(image_bytes).decode()
    # details = _call_openai_api(image_b64)
    details = _call_openai_api_mock(image_b64)
    json_block = re.search(r"```json(.*?)```", details, re.S) 
    book_details = {}
    if json_block:
        book_details = json.loads(json_block.group(1).strip())
        book_details['image'] = image_b64
    
        return book_details
    
    raise ValueError("No JSON block found in the response.")
