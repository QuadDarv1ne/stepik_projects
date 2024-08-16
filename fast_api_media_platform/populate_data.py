import json
from app.database import engine
from app.models import Base, Category, Genre

# Создаем таблицы
Base.metadata.create_all(bind=engine)

from sqlalchemy.orm import Session
from app.database import SessionLocal


def populate_categories():
    with open("static/categories.json") as f:
        categories = json.load(f)

    db: Session = SessionLocal()
    try:
        for category in categories:
            db_category = Category(name=category["name"])
            db.add(db_category)
        db.commit()
    finally:
        db.close()


def populate_genres():
    with open("static/genres.json") as f:
        genres = json.load(f)

    db: Session = SessionLocal()
    try:
        for genre in genres:
            db_genre = Genre(name=genre["name"])
            db.add(db_genre)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    populate_categories()
    populate_genres()
