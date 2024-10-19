from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import get_db
from app.utils import create_access_token
from passlib.context import CryptContext

router = APIRouter()

# Инициализируем контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Указываем, как будет работать OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Регистрация нового пользователя
@router.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли уже пользователь
    existing_user = crud.get_user_by_username(db, username=user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    # Хешируем пароль и создаем пользователя
    hashed_password = pwd_context.hash(user.password)
    return crud.create_user(db=db, username=user.username, hashed_password=hashed_password)

# Логин пользователя
@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")

    # Создаем токен для пользователя
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
