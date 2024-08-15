'''
Описание класса книги:
1️⃣ id: уникальный идентификатор книги.
2️⃣ title: название книги.
3️⃣ author: автор книги.
4️⃣ publication_year: год публикации книги.
5️⃣ description: описание книги.
6️⃣ image: ссылка на изображение обложки книги.
'''

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./books.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    publication_year = Column(Integer)
    description = Column(String)
    image = Column(String)

Base.metadata.create_all(bind=engine)
