from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# Схемы для категорий

class CategoryBase(BaseModel):
    name: str = Field(..., example="Pop")

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

# Схемы для жанров

class GenreBase(BaseModel):
    name: str = Field(..., example="Rock")

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int

    class Config:
        from_attributes = True

# Схемы для медиа файлов

class MediaFileBase(BaseModel):
    name_music: str = Field(..., example="Song Title")
    description: str = Field(..., example="A great song description.")
    file_name: str = Field(..., example="song.mp3")
    file_path: str = Field(..., example="/media/files/song.mp3")
    cover_image_path: str = Field(..., example="/media/covers/cover.jpg")
    category_id: int = Field(..., example=1)
    genre_id: int = Field(..., example=2)
    youtube_url: Optional[str] = Field(None, example="https://www.youtube.com/watch?v=xyz")
    rutube_url: Optional[str] = Field(None, example="https://rutube.ru/video/xyz")
    plvideo_url: Optional[str] = Field(None, example="https://pl.video/xyz")

class MediaFileCreate(MediaFileBase):
    pass

class MediaFile(MediaFileBase):
    id: int

    class Config:
        from_attributes = True

# Схемы для пользователей

class UserBase(BaseModel):
    username: str = Field(..., max_length=50, example="user123")
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, example="strongpassword")

class UserRead(UserBase):
    id: int
    is_active: bool
    role_id: Optional[int]

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr]
    password: Optional[str] = Field(None, min_length=6)
    is_active: Optional[bool]

# Схемы для ролей пользователей

class RoleBase(BaseModel):
    name: str = Field(..., max_length=50, example="user")

class RoleRead(RoleBase):
    id: int

    class Config:
        from_attributes = True        
