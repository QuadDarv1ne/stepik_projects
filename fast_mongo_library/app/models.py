from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    published_year: int
    genre: str
    description: str

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: str

    class Config:
        from_attributes = True
