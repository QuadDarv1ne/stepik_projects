from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from werkzeug.security import generate_password_hash, check_password_hash

class MediaFile(Base):
    __tablename__ = "media_files"

    id = Column(Integer, primary_key=True, index=True)
    name_music = Column(String, index=True)

    # Поле для описания музыкальной композиции
    description = Column(Text, nullable=True)

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
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)  # Поле для деактивации пользователя, если нужно
    role_id = Column(Integer, ForeignKey("roles.id"))

    role = relationship("Role", back_populates="users")

    def set_password(self, password):
        """Сохраняет хэшированный пароль."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Проверяет пароль."""
        return check_password_hash(self.password_hash, password)

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)  # Например, "admin", "user", и т.д.

    users = relationship("User", back_populates="role")
