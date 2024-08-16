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
