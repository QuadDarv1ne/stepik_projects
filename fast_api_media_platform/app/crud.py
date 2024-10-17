from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import models
from app.models import MediaFile
from app.schemas import MediaFileCreate

def get_media_files(db: Session):
    """Получить все медиафайлы"""
    return db.query(models.MediaFile).all()

def create_media_file(db: Session, name_music: str, file_name: str, file_path: str, cover_image_path: str, 
                      category_id: int, genre_id: int, youtube_url: str = None, 
                      rutube_url: str = None, plvideo_url: str = None):
    
    """Создать новый медиафайл с URL"""
    new_media_file = MediaFile(
        name_music=name_music,
        file_name=file_name,
        file_path=file_path,
        cover_image_path=cover_image_path,
        category_id=category_id,
        genre_id=genre_id,
        youtube_url=youtube_url,
        rutube_url=rutube_url,
        plvideo_url=plvideo_url
    )
    db.add(new_media_file)
    db.commit()
    db.refresh(new_media_file)
    return new_media_file

def get_media_file_by_id(db: Session, media_id: int):
    """Получить медиафайл по его ID"""
    return db.query(models.MediaFile).filter(models.MediaFile.id == media_id).first()

def get_categories(db: Session):
    """Получить все категории"""
    return db.query(models.Category).all()

def get_genres(db: Session):
    """Получить все жанры"""
    return db.query(models.Genre).all()

def create_category(db: Session, name: str):
    """Создать новую категорию"""
    db_category = models.Category(name=name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def create_genre(db: Session, name: str):
    """Создать новый жанр"""
    db_genre = models.Genre(name=name)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

def update_media_file(db: Session, media_id: int, name_music: str, category_id: int, genre_id: int, youtube_url: str, rutube_url: str, plvideo_url: str):
    media_file = db.query(MediaFile).filter(MediaFile.id == media_id).first()
    if media_file is None:
        raise HTTPException(status_code=404, detail="Медиа файл не найден")

    media_file.name_music = name_music
    media_file.category_id = category_id
    media_file.genre_id = genre_id
    media_file.youtube_url = youtube_url
    media_file.rutube_url = rutube_url
    media_file.plvideo_url = plvideo_url

    db.commit()
    db.refresh(media_file)
    return media_file
