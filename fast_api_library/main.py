from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from models import Book, SessionLocal
from pydantic import BaseModel
import json

app = FastAPI()

# Dependency для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic модель для API
class BookCreate(BaseModel):
    title: str
    author: str
    publication_year: int
    description: str
    image: str

@app.get("/books/", response_model=List[BookCreate])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = db.query(Book).offset(skip).limit(limit).all()
    return books

@app.get("/books/{book_id}", response_model=BookCreate)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена") # Book not found
    return book

@app.post("/books/", response_model=BookCreate)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.put("/books/{book_id}", response_model=BookCreate)
def update_book(book_id: int, updated_book: BookCreate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена") # Book not found
    for key, value in updated_book.dict().items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book

@app.delete("/books/{book_id}", response_model=BookCreate)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена") # Book not found
    db.delete(book)
    db.commit()
    return book


@app.post("/update_books_from_json/")
def update_books_from_json(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(_update_books_from_json, db)
    return {"message": "Update started in the background"}


def _update_books_from_json(db: Session):
    try:
        with open('data/books.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Сначала удаляем все книги
        db.query(Book).delete()

        # Добавляем книги из JSON
        for book_data in data:
            book = Book(**book_data)
            db.add(book)

        db.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()

# TODO: Заметки
## 1️⃣ GET /books/
## 2️⃣ GET /books/{book_id}
## 3️⃣ POST /books/
## 4️⃣ PUT /books/{book_id}
## 5️⃣ DELETE /books/{book_id}