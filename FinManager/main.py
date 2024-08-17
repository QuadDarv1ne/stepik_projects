from fastapi import FastAPI, Depends, HTTPException, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional
from models import User as UserModel
from schemas import UserCreate
from crud import create_user, get_user_by_email, get_transactions, get_budgets
from auth import authenticate_user, create_access_token, get_current_user, get_password_hash

import logging

app = FastAPI()

# Конфигурация шаблонов и статических файлов
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Конфигурация OAuth2 для авторизации
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

logging.basicConfig(level=logging.INFO)

# Функция получения текущего пользователя из токена в куки
async def get_current_user_from_token(request: Request, token: str = Depends(oauth2_scheme)) -> UserModel:
    token = request.cookies.get("access_token")  # Извлекаем токен из куки
    if not token:
        raise HTTPException(status_code=401, detail="Token not found")

    # Убираем префикс 'Bearer ' и проверяем корректность токена
    token = token.split(" ")[1] if " " in token else token
    try:
        user = await get_current_user(token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return user
    except HTTPException:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

# Маршруты

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Главная страница до авторизации"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard(request: Request, current_user: UserModel = Depends(get_current_user_from_token)):
    """Личный кабинет пользователя"""
    return templates.TemplateResponse("dashboard.html", {"request": request, "title": "Личный кабинет", "user": current_user})

@app.get("/register", response_class=HTMLResponse)
async def get_register(request: Request):
    """Форма регистрации"""
    return templates.TemplateResponse("register.html", {"request": request, "title": "Регистрация"})

@app.post("/register", response_class=HTMLResponse)
async def post_register(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    """Обработка данных формы регистрации"""
    existing_user = await get_user_by_email(email)
    if existing_user:
        return templates.TemplateResponse("register.html", {"request": request, "title": "Регистрация", "error": "Email уже зарегистрирован"})

    hashed_password = get_password_hash(password)  # Хешируем пароль
    user_obj = UserCreate(username=username, email=email, password=hashed_password)  # Передаем хешированный пароль
    await create_user(user_obj)

    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

@app.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    """Форма входа"""
    return templates.TemplateResponse("login.html", {"request": request, "title": "Вход"})

@app.post("/login", response_class=HTMLResponse)
async def post_login(request: Request, identifier: str = Form(...), password: str = Form(...)):
    """Обработка данных формы входа"""
    user = await authenticate_user(identifier, password)
    if not user:
        logging.info("Login failed for user: %s", identifier)
        return templates.TemplateResponse("login.html", {"request": request, "title": "Вход", "error": "Неверные учетные данные"})

    access_token = create_access_token(data={"sub": user.email})
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)

    logging.info("Login successful for user: %s", identifier)
    return response

@app.get("/logout")
async def logout():
    """Выход из системы"""
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("access_token")
    return response

@app.get("/transactions", response_class=HTMLResponse)
async def read_transactions(request: Request, current_user: UserModel = Depends(get_current_user_from_token)):
    """Страница транзакций"""
    transactions = await get_transactions(current_user.id)  # Используем current_user.id для получения транзакций
    return templates.TemplateResponse("transactions.html", {"request": request, "title": "Транзакции", "transactions": transactions})

@app.get("/budgets", response_class=HTMLResponse)
async def read_budgets(request: Request, current_user: UserModel = Depends(get_current_user_from_token)):
    """Страница бюджетов"""
    budgets = await get_budgets(current_user.id)  # Используем current_user.id для получения бюджетов
    return templates.TemplateResponse("budgets.html", {"request": request, "title": "Бюджеты", "budgets": budgets})

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Обработка исключений"""
    return templates.TemplateResponse("error.html", {"request": request, "detail": exc.detail}, status_code=exc.status_code)


'''
Шаблоны и статические файлы: Используем Jinja2Templates для подключения шаблонов и StaticFiles для подключения статических файлов (CSS, JS, изображения).

Маршруты:
    GET / — главная страница приложения.
    GET /register и POST /register — форма регистрации и обработка данных формы.
    GET /login и POST /login — форма входа и обработка данных формы.
    GET /logout — выход из системы.
    GET /transactions — страница для отображения транзакций пользователя.
    GET /budgets — страница для отображения бюджетов пользователя.

Функции:
    read_root — отображает главную страницу.
    get_register и post_register — показывают форму регистрации и обрабатывают данные.
    get_login и post_login — показывают форму входа и обрабатывают данные.
    logout — удаляет куки с токеном авторизации.
    read_transactions и read_budgets — отображают страницы с транзакциями и бюджетами.
    
Подключение к базе данных и функции CRUD:
Убедитесь, что в crud.py реализованы функции, такие как create_user, get_user_by_email, create_transaction, get_transactions, create_budget, и get_budgets.

Также убедитесь, что в auth.py содержатся функции для аутентификации пользователя и создания токенов.
'''