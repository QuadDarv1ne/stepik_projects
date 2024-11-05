from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import Optional

# Схемы для категорий

class CategoryBase(BaseModel):
    name: str = Field(..., example="Pop", description="Название категории")

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

# Схемы для жанров

class GenreBase(BaseModel):
    name: str = Field(..., example="Rock", description="Название жанра")

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int

    class Config:
        from_attributes = True

# Схемы для медиа файлов

class MediaFileBase(BaseModel):
    name_music: str = Field(..., example="Song Title", description="Название музыкального произведения")
    description: Optional[str] = Field(None, example="A great song description.", description="Описание композиции")
    file_name: str = Field(..., example="song.mp3", description="Имя файла медиа")
    file_path: str = Field(..., example="/media/files/song.mp3", description="Путь к файлу медиа")
    cover_image_path: Optional[str] = Field(None, example="/media/covers/cover.jpg", description="Путь к изображению обложки")
    category_id: int = Field(..., example=1, description="ID категории")
    genre_id: int = Field(..., example=2, description="ID жанра")
    youtube_url: Optional[HttpUrl] = Field(None, example="https://www.youtube.com/watch?v=xyz", description="Ссылка на YouTube")
    rutube_url: Optional[HttpUrl] = Field(None, example="https://rutube.ru/video/xyz", description="Ссылка на RuTube")
    plvideo_url: Optional[HttpUrl] = Field(None, example="https://pl.video/xyz", description="Ссылка на Plvideo")

class MediaFileCreate(MediaFileBase):
    pass

class MediaFile(MediaFileBase):
    id: int

    class Config:
        from_attributes = True

# Схемы для пользователей

class UserBase(BaseModel):
    username: str = Field(..., max_length=50, example="user123", description="Имя пользователя")
    email: EmailStr = Field(..., example="user@example.com", description="Электронная почта пользователя")

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserRead(UserBase):
    id: int
    is_active: bool = Field(..., description="Статус активности пользователя")
    role_id: Optional[int] = Field(None, description="ID роли пользователя")
    profile_image_path: Optional[str] = Field(None, example="/profile_images/user123.jpg", description="Путь к фотографии профиля")

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=50, description="Новое имя пользователя")
    email: Optional[EmailStr] = Field(None, description="Новая электронная почта пользователя")
    password: Optional[str] = Field(None, min_length=6, description="Новый пароль пользователя")
    is_active: Optional[bool] = Field(None, description="Новый статус активности пользователя")
    profile_image_path: Optional[str] = Field(None, example="/profile_images/new_user123.jpg", description="Новый путь к фотографии профиля")

# Схемы для ролей пользователей

class RoleBase(BaseModel):
    name: str = Field(..., max_length=50, example="user", description="Название роли")

class RoleRead(RoleBase):
    id: int

    class Config:
        from_attributes = True
