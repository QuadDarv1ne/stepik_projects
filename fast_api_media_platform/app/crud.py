from sqlalchemy.orm import Session
from app import models
from app.models import MediaFile
from app.schemas import MediaFileCreate

def get_media_files(db: Session):
    return db.query(models.MediaFile).all()

def create_media_file(db: Session, name_music: str, file_name: str, file_path: str, cover_image_path: str, category_id: int, genre_id: int):
    new_media_file = MediaFile(
        name_music=name_music,
        file_name=file_name,
        file_path=file_path,
        cover_image_path=cover_image_path,
        category_id=category_id,
        genre_id=genre_id
    )
    db.add(new_media_file)
    db.commit()
    db.refresh(new_media_file)
    return new_media_file


def get_categories(db: Session):
    return db.query(models.Category).all()

def get_genres(db: Session):
    return db.query(models.Genre).all()

def create_category(db: Session, name: str):
    db_category = models.Category(name=name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def create_genre(db: Session, name: str):
    db_genre = models.Genre(name=name)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

def get_media_file_by_id(db: Session, media_id: int):
    return db.query(models.MediaFile).filter(models.MediaFile.id == media_id).first()
