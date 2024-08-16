from pydantic import BaseModel
from typing import Optional

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

class MediaFileCreate(MediaFileBase):
    pass

class MediaFile(MediaFileBase):
    id: int

    class Config:
        from_attributes = True
