from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class MediaFile(Base):
    __tablename__ = "media_files"

    id = Column(Integer, primary_key=True, index=True)
    name_music = Column(String, index=True)
    file_name = Column(String, index=True)
    file_path = Column(String)
    cover_image_path = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))
    genre_id = Column(Integer, ForeignKey("genres.id"))

    # Новые поля для различных видео URL
    youtube_url = Column(String(255), nullable=True)
    rutube_url = Column(String(255), nullable=True)
    plvideo_url = Column(String(255), nullable=True)
    
    category = relationship("Category", back_populates="media_files")
    genre = relationship("Genre", back_populates="media_files")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    media_files = relationship("MediaFile", back_populates="category")

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    media_files = relationship("MediaFile", back_populates="genre")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    profile_pic = Column(String, default='default.jpg')  # Путь к фотографии профиля

    favorites = relationship("Favorite", back_populates="owner")

class Music(Base):
    __tablename__ = "music"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    artist = Column(String)

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    music_id = Column(Integer, ForeignKey("music.id"))

    owner = relationship("User", back_populates="favorites")
