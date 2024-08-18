from typing import List
from pydantic import BaseModel

class BookInDB(BaseModel):
    id: str
    title: str
    author: str
    published_year: int
    genre: str
    description: str

    class Config:
        from_attributes = True

class BookInList(BaseModel):
    books: List[BookInDB]
