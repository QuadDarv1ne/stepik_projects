from pydantic import BaseModel, EmailStr
from typing import Optional, List

# Схемы для категорий
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

# Схемы для жанров
class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int

    class Config:
        from_attributes = True

# Схемы для медиафайлов
class MediaFileBase(BaseModel):
    name_music: str
    file_name: str
    file_path: str
    cover_image_path: str
    category_id: int
    genre_id: int
    youtube_url: Optional[str] = None
    rutube_url: Optional[str] = None
    plvideo_url: Optional[str] = None

class MediaFileCreate(MediaFileBase):
    pass

class MediaFile(MediaFileBase):
    id: int

    class Config:
        from_attributes = True

# Схемы для пользователей
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    profile_pic: Optional[str] = None

    class Config:
        from_attributes = True

class UserOut(User):
    # Можно расширить или изменить User для вывода, если нужно
    pass

# Схемы для музыки
class Music(BaseModel):
    id: int
    title: str
    artist: str

    class Config:
        from_attributes = True

# Схемы для избранного
class FavoriteCreate(BaseModel):
    music_id: int

class FavoriteOut(BaseModel):
    id: int
    user_id: int
    music_id: int

    class Config:
        from_attributes = True
