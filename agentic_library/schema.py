from pydantic import BaseModel, Field
from typing import Optional

class Book(BaseModel):
    """
    Represents a book in the personal library system.
    Stores metadata such as user ID, unique book ID, title, author, tagline, image, and genre.
    Used for database operations and UI display.
    """
    user_id: str = Field(..., description="ID of the user who owns the book")
    uuid: str = Field(..., description="Unique identifier for the book")
    title: str = Field(..., description="Title of the book")
    author: str = Field(..., description="Author of the book")
    tagline: Optional[str] = Field(None, description="Tagline or short description of the book")
    image: Optional[bytes] = Field(None, description="Image data as bytes")
    genre: Optional[str] = Field(None, description="Genre or category of the book")
