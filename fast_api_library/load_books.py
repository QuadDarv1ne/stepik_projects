import json
from sqlalchemy.orm import Session
from models import Book, SessionLocal

def load_books_from_json(session: Session, json_file_path: str):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        books = json.load(f)
        for book in books:
            db_book = Book(
                id=book['id'],
                title=book['title'],
                author=book['author'],
                publication_year=book['publication_year'],
                description=book['description'],
                image=book['image']
            )
            session.add(db_book)
        session.commit()

def save_books_to_db(books, db: Session):
    for book_data in books:
        book = Book(**book_data)
        db.add(book)
    db.commit()

def main():
    books = load_books_from_json("data/books.json")
    db = SessionLocal()
    save_books_to_db(books, db)
    db.close()

if __name__ == "__main__":
    main()
