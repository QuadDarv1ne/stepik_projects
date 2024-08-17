from pydantic import BaseModel, EmailStr, Field, validator
from bson import ObjectId
from typing import Optional

class User(BaseModel):
    id: Optional[str] = None
    username: str
    email: EmailStr
    password: str

    @validator('id', pre=True, always=True)
    def check_object_id(cls, v):
        if v and not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return v

class Transaction(BaseModel):
    id: Optional[str] = None
    type: str
    amount: float
    description: Optional[str] = None
    date: Optional[str] = None

    @validator('id', pre=True, always=True)
    def check_object_id(cls, v):
        if v and not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return v

class Budget(BaseModel):
    id: Optional[str] = None
    name: str
    limit: float
    current_spend: float

    @validator('id', pre=True, always=True)
    def check_object_id(cls, v):
        if v and not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return v
