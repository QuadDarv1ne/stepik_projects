from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr

class TransactionCreate(BaseModel):
    type: str
    amount: float
    description: Optional[str] = None
    date: Optional[str] = None

class TransactionResponse(BaseModel):
    id: str
    type: str
    amount: float
    description: Optional[str] = None
    date: Optional[str] = None

class BudgetCreate(BaseModel):
    name: str
    limit: float

class BudgetResponse(BaseModel):
    id: str
    name: str
    limit: float
    current_spend: float
