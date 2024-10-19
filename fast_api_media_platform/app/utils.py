from datetime import datetime, timedelta
from jose import JWTError, jwt
from itsdangerous import URLSafeTimedSerializer
from fastapi import Depends

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

serializer = URLSafeTimedSerializer(SECRET_KEY)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def generate_reset_token(email: str) -> str:
    return serializer.dumps(email, salt="password-reset-salt")

def verify_reset_token(token: str) -> str:
    try:
        email = serializer.loads(token, salt="password-reset-salt", max_age=3600)  # Токен действителен 1 час
    except Exception:
        return None
    return email
