from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from werkzeug.security import generate_password_hash, check_password_hash


class MediaFile(Base):
    __tablename__ = "media_files"

    id = Column(Integer, primary_key=True, index=True)
    name_music = Column(String(100), nullable=False, index=True, comment="Название музыкального произведения")
    description = Column(Text, nullable=True, comment="Описание музыкальной композиции")
    
    file_name = Column(String, nullable=False, index=True, comment="Имя файла")
    file_path = Column(String, nullable=False, comment="Путь к файлу")
    cover_image_path = Column(String, nullable=True, comment="Путь к обложке композиции")
    
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False)

    # Дополнительные поля для ссылок на видео
    youtube_url = Column(String(255), nullable=True, comment="Ссылка на YouTube")
    rutube_url = Column(String(255), nullable=True, comment="Ссылка на RuTube")
    plvideo_url = Column(String(255), nullable=True, comment="Ссылка на Plvideo")
    
    category = relationship("Category", back_populates="media_files")
    genre = relationship("Genre", back_populates="media_files")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True, index=True, comment="Название категории")
    
    media_files = relationship("MediaFile", back_populates="category", cascade="all, delete")


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True, index=True, comment="Название жанра")
    
    media_files = relationship("MediaFile", back_populates="genre", cascade="all, delete")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True, comment="Имя пользователя")
    email = Column(String(100), unique=True, nullable=False, index=True, comment="Электронная почта")
    password_hash = Column(String(128), nullable=False, comment="Хешированный пароль")
    profile_image_path = Column(String, nullable=True, comment="Путь к фотографии профиля")
    is_active = Column(Boolean, default=True, comment="Статус активности пользователя")
    
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
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
    name = Column(String(50), unique=True, nullable=False, index=True, comment="Название роли, например, admin, user")

    users = relationship("User", back_populates="role", cascade="all, delete")
