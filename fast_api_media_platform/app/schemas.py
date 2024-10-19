from pydantic import BaseModel, EmailStr
from typing import List, Optional

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int

    class Config:
        from_attributes = True

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


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    profile_pic: str

    class Config:
        from_attributes = True

class Music(BaseModel):
    id: int
    title: str
    artist: str

    class Config:
        from_attributes = True

class FavoriteCreate(BaseModel):
    user_id: int
    music_id: int

class Favorite(BaseModel):
    id: int
    user_id: int
    music_id: int

    class Config:
        from_attributes = True
