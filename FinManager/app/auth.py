import hashlib
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
from crud import get_user_by_email, get_user_by_username
from models import User

import logging

logger = logging.getLogger(__name__)

# Конфигурация
SECRET_KEY = "Hm9rRyDurmK+aO49ZTCr61rCzOcmP7q6kur5C4nZD94=" # openssl rand -base64 32
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Создание контекста для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Настройка OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Модели данных
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Функции для работы с паролями
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка правильности пароля."""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logging.error(f"Password verification error: {e}")
        raise

def get_password_hash(password: str) -> str:
    """Хеширование пароля."""
    return pwd_context.hash(password)

# Функции для работы с JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            logger.error("Email not found in token payload")
            raise credentials_exception
        user = await get_user_by_email(email)
        if user is None:
            logger.error(f"User with email {email} not found")
            raise credentials_exception
    except JWTError as e:
        logger.error(f"JWTError: {e}")
        raise credentials_exception
    return user

async def authenticate_user(identifier: str, password: str):
    if "@" in identifier and "." in identifier:
        user = await get_user_by_email(identifier)
    else:
        user = await get_user_by_username(identifier)

    if not user:
        return False

    if not verify_password(password, user.password):
        return False

    return user
