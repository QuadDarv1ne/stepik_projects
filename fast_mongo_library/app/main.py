from typing import List
from fastapi import FastAPI, HTTPException
from .models import BookCreate, Book
from .crud import create_book, get_books, get_book, update_book, delete_book

app = FastAPI()

@app.post("/books/", response_model=Book)
async def api_create_book(book: BookCreate):
    return await create_book(book)

@app.get("/books/", response_model=List[Book])
async def api_get_books():
    return await get_books()

@app.get("/books/{book_id}", response_model=Book)
async def api_get_book(book_id: str):
    book = await get_book(book_id)
    if book:
        return book
    raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")

@app.put("/books/{book_id}", response_model=Book)
async def api_update_book(book_id: str, book: BookCreate):
    updated_book = await update_book(book_id, book)
    if updated_book:
        return updated_book
    raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")

@app.delete("/books/{book_id}", response_model=dict)
async def api_delete_book(book_id: str):
    result = await delete_book(book_id)
    if result["status"] == "Book deleted":
        return result
    raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
