from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Table
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

# Промежуточная таблица для избранного
favorite_music = Table(
    'favorite_music',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('music_id', Integer, ForeignKey('music.id'))
)

class MediaFile(Base):
    __tablename__ = "media_files"

    id = Column(Integer, primary_key=True, index=True)
    name_music = Column(String(100), index=True)
    filename = Column(String(100), index=True)
    file_path = Column(String)
    cover_image_path = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))
    genre_id = Column(Integer, ForeignKey("genres.id"))
    youtube_url = Column(String(255), nullable=True)
    rutube_url = Column(String(255), nullable=True)
    plvideo_url = Column(String(255), nullable=True)

    category = relationship("Category", back_populates="media_files")
    genre = relationship("Genre", back_populates="media_files")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)

    media_files = relationship("MediaFile", back_populates="category")

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)

    media_files = relationship("MediaFile", back_populates="genre")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(128))  # Длина хешированного пароля
    profile_pic = Column(String, default='default.jpg')  # Путь к фотографии профиля
    is_active = Column(Boolean, default=True)

    favorites = relationship("Favorite", back_populates="owner")

class Music(Base):
    __tablename__ = "music"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    artist = Column(String(100))
    duration = Column(Integer)  # Продолжительность в секундах
    release_date = Column(DateTime)  # Дата выхода

    favorites = relationship("Favorite", back_populates="music")

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    music_id = Column(Integer, ForeignKey("music.id"))

    owner = relationship("User", back_populates="favorites")
    music = relationship("Music", back_populates="favorites")
