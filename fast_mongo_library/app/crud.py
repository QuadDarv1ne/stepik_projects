from typing import List, Dict, Any
from bson import ObjectId
from .database import collection
from .models import BookCreate, Book
from fastapi import HTTPException

async def create_book(book: BookCreate) -> Book:
    book_dict = book.dict()
    result = await collection.insert_one(book_dict)
    new_book = await collection.find_one({"_id": result.inserted_id})
    return Book(**new_book, id=str(new_book["_id"]))

async def get_book(book_id: str):
    try:
        book_id = ObjectId(book_id)  # Преобразование строки в ObjectId
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid book ID format")

    book = await collection.find_one({"_id": book_id})
    if book:
        # Преобразование BSON документа в Pydantic модель
        return Book(**{**book, 'id': str(book['_id'])})
    raise HTTPException(status_code=404, detail="Book not found")

async def get_books():
    books = []
    async for book in collection.find():
        # Преобразование BSON документа в Pydantic модель
        books.append(Book(**{**book, 'id': str(book['_id'])}))
    return books

async def update_book(book_id: str, book: BookCreate) -> Book:
    result = await collection.update_one(
        {"_id": ObjectId(book_id)},
        {"$set": book.dict()}
    )
    if result.matched_count:
        updated_book = await collection.find_one({"_id": ObjectId(book_id)})
        return Book(**updated_book, id=str(updated_book["_id"]))
    return None

async def delete_book(book_id: str) -> Dict[str, Any]:
    result = await collection.delete_one({"_id": ObjectId(book_id)})
    if result.deleted_count:
        return {"status": "Book deleted"}
    return {"status": "Book not found"}
