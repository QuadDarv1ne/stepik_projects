import logging
from fastapi import FastAPI, Depends, HTTPException, Request, Form, File, UploadFile, APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from starlette.requests import Request
from app.models import MediaFile
from starlette.responses import HTMLResponse

from app import models, crud, schemas
from app.database import engine, SessionLocal
from werkzeug.utils import secure_filename
import os

from typing import Optional

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Инициализация FastAPI
app = FastAPI()

# Настройка обслуживания статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Создание таблиц в базе данных
models.Base.metadata.create_all(bind=engine)

# Получение сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Middleware для кэширования статических файлов
@app.middleware("http")
async def add_cache_header(request, call_next):
    response = await call_next(request)
    if request.url.path.startswith("/static"):
        # Установите время жизни кэша в 600 секунд (10 минут)
        response.headers["Cache-Control"] = "public, max-age=600"
    return response


@app.get("/")
async def read_root(request: Request, db: Session = Depends(get_db)):
    try:
        media_files = crud.get_media_files(db)
        return templates.TemplateResponse("index.html", {"request": request, "media_files": media_files})
    except SQLAlchemyError as e:
        logger.error(f"Ошибка базы данных: {e}")
        raise HTTPException(status_code=500, detail="Ошибка базы данных")


@app.get("/upload")
async def upload_form(request: Request, db: Session = Depends(get_db)):
    try:
        categories = crud.get_categories(db)
        genres = crud.get_genres(db)
        return templates.TemplateResponse("upload.html",
                                          {"request": request, "categories": categories, "genres": genres})
    except SQLAlchemyError as e:
        logger.error(f"Ошибка базы данных: {e}")
        raise HTTPException(status_code=500, detail="Ошибка базы данных")


@app.post("/upload")
async def upload_file(
        name_music: str = Form(...),
        description: str = Form(...),
        music_file: UploadFile = File(...),
        cover_file: UploadFile = File(...),
        category_id: int = Form(...),
        genre_id: int = Form(...),
        youtube_url: str = Form(None),   # Новое поле для YouTube
        rutube_url: str = Form(None),    # Новое поле для Rutube
        plvideo_url: str = Form(None),   # Новое поле для Plvideo
        db: Session = Depends(get_db)
):
    try:
        # Обеспечить безопасность имен файлов
        music_filename = secure_filename(music_file.filename)
        cover_filename = secure_filename(cover_file.filename)

        # Определение путей для сохранения файлов
        music_dir = os.path.join("static", "music")
        cover_dir = os.path.join("static", "covers")

        # Создать директории, если их нет
        os.makedirs(music_dir, exist_ok=True)
        os.makedirs(cover_dir, exist_ok=True)

        music_file_path = os.path.join(music_dir, music_filename)
        cover_file_path = os.path.join(cover_dir, cover_filename)

        # Сохранение файлов
        with open(music_file_path, "wb") as f:
            f.write(await music_file.read())

        with open(cover_file_path, "wb") as f:
            f.write(await cover_file.read())

        # Добавление записи в базу данных
        crud.create_media_file(
            db=db,
            name_music=name_music,
            description=description,
            file_name=music_filename,
            file_path=music_file_path,
            cover_image_path=cover_file_path,
            category_id=category_id,
            genre_id=genre_id,
            youtube_url=youtube_url,     # Передаем YouTube URL
            rutube_url=rutube_url,       # Передаем Rutube URL
            plvideo_url=plvideo_url      # Передаем Plvideo URL
        )
        return RedirectResponse("/", status_code=303)
    except SQLAlchemyError as e:
        logger.error(f"Ошибка базы данных: {e}")
        raise HTTPException(status_code=500, detail="Ошибка базы данных")
    except Exception as e:
        logger.error(f"Ошибка загрузки файла: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка загрузки файла: {e}")


@app.get("/create-category")
async def create_category_form(request: Request):
    return templates.TemplateResponse("create_category.html", {"request": request})


@app.post("/create-category")
async def create_category(name: str = Form(...), db: Session = Depends(get_db)):
    try:
        crud.create_category(db=db, name=name)
        return RedirectResponse("/", status_code=303)
    except SQLAlchemyError as e:
        logger.error(f"Ошибка базы данных: {e}")
        raise HTTPException(status_code=500, detail="Ошибка базы данных")


@app.get("/create-genre")
async def create_genre_form(request: Request):
    return templates.TemplateResponse("create_genre.html", {"request": request})


@app.post("/create-genre")
async def create_genre(name: str = Form(...), db: Session = Depends(get_db)):
    try:
        crud.create_genre(db=db, name=name)
        return RedirectResponse("/", status_code=303)
    except SQLAlchemyError as e:
        logger.error(f"Ошибка базы данных: {e}")
        raise HTTPException(status_code=500, detail="Ошибка базы данных")


@app.get("/media/{media_id}")
async def read_media(request: Request, media_id: int, db: Session = Depends(get_db)):
    try:
        media_file = crud.get_media_file_by_id(db, media_id)  # Получите данные из базы данных
        headers = {"Cache-Control": "public, max-age=86400"}  # 1 день
        if media_file is None:
            raise HTTPException(status_code=404, detail="Медиа файл не найден")
        return templates.TemplateResponse("media_detail.html", {"request": request, "media_file": media_file})
    except SQLAlchemyError as e:
        logger.error(f"Ошибка базы данных: {e}")
        raise HTTPException(status_code=500, detail="Ошибка базы данных")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        raise HTTPException(status_code=500, detail="Ошибка сервера")


@app.on_event("shutdown")
def cleanup_temp_files():
    temp_dir = '/path/to/temp/dir'
    for filename in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Ошибка при удалении файла: {e}")


@app.get("/edit-media/{media_id}")
async def edit_media_form(request: Request, media_id: int, db: Session = Depends(get_db)):
    try:
        media_file = crud.get_media_file_by_id(db, media_id)  # Получите медиа файл по ID
        if media_file is None:
            raise HTTPException(status_code=404, detail="Медиа файл не найден")
        categories = crud.get_categories(db)
        genres = crud.get_genres(db)
        return templates.TemplateResponse("edit_media.html", {"request": request, "media_file": media_file, "categories": categories, "genres": genres})
    except SQLAlchemyError as e:
        logger.error(f"Ошибка базы данных: {e}")
        raise HTTPException(status_code=500, detail="Ошибка базы данных")


@app.post("/edit-media/{media_id}")
async def update_media(
        media_id: int,
        name_music: str = Form(...),
        description: str = Form(...),
        category_id: int = Form(...),
        genre_id: int = Form(...),
        youtube_url: str = Form(None), 
        rutube_url: str = Form(None),   
        plvideo_url: str = Form(None),
        db: Session = Depends(get_db)
):
    try:
        media_file = crud.get_media_file_by_id(db, media_id)
        if media_file is None:
            raise HTTPException(status_code=404, detail="Медиа файл не найден")

        # Обновление данных в базе данных
        crud.update_media_file(
            db=db,
            media_id=media_id,
            name_music=name_music,
            description=description,
            category_id=category_id,
            genre_id=genre_id,
            youtube_url=youtube_url,
            rutube_url=rutube_url,
            plvideo_url=plvideo_url
        )
        return RedirectResponse(f"/media/{media_id}", status_code=303)  # Перенаправление на страницу медиа
    except SQLAlchemyError as e:
        logger.error(f"Ошибка базы данных: {e}")
        raise HTTPException(status_code=500, detail="Ошибка базы данных")
    except Exception as e:
        logger.error(f"Ошибка обновления данных: {e}")
        raise HTTPException(status_code=500, detail="Ошибка обновления данных")


@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/contact")
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@app.get("/privacy")
async def privacy(request: Request):
    return templates.TemplateResponse("privacy.html", {"request": request})


@app.get("/api/categories")
async def get_categories(db: Session = Depends(get_db)):
    categories = crud.get_categories(db)
    return categories

@app.get("/api/genres")
async def get_genres(db: Session = Depends(get_db)):
    genres = crud.get_genres(db)
    return genres

@app.get("/search")
async def search(
    request: Request,
    query: Optional[str] = None,
    category_id: Optional[str] = None,
    genre_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        # Преобразуем category_id и genre_id в целые числа, если они не пустые
        category_id = int(category_id) if category_id and category_id.isdigit() else None
        genre_id = int(genre_id) if genre_id and genre_id.isdigit() else None
        
        # Если все параметры пустые, вернуть все карточки музыки
        if not query and category_id is None and genre_id is None:
            media_files = crud.get_media_files(db)
        else:
            media_files = crud.search_media_files(db, query, category_id, genre_id)
        
        return templates.TemplateResponse("index.html", {"request": request, "media_files": media_files})
    except SQLAlchemyError as e:
        logger.error(f"Ошибка базы данных: {e}")
        raise HTTPException(status_code=500, detail="Ошибка базы данных")

<<<<<<< HEAD
@app.get("/register", name="register")
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)  # Получаем сессию базы данных
):
    user_create = schemas.UserCreate(username=username, email=email, password=password)
    
    try:
        crud.create_user(db=db, user=user_create)  # Создаем пользователя
        return RedirectResponse(url="/login", status_code=303)  # Перенаправить на страницу входа
    except ValueError as ve:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": str(ve)  # Показать сообщение об ошибке на странице регистрации
        })
    except Exception as e:
        logger.error(f"Ошибка при регистрации пользователя: {e}")
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Не удалось создать пользователя. Пожалуйста, попробуйте снова."
        })

@app.get("/login", response_class=templates.TemplateResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    user = await crud.authenticate_user(username=username, password=password)
    if not user:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Неверное имя пользователя или пароль"
        })
    
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="user_id", value=str(user.id))  # Store user id in cookies
    return response

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"SQLAlchemy ошибка: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Ошибка базы данных"})

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Ошибка: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Внутренняя ошибка сервера"})

# Функция для удаления директорий __pycache__ (если необходимо)
remove_pycache_dirs()
=======
'''
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Максимальный размер файла 16MB
allowed_extensions = {'mp3', 'wav', 'jpg', 'png'}
'''

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

@app.post("/login")
async def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    # Здесь логика авторизации
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})

@app.post("/register")
async def register_post(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    # Здесь логика регистрации
    return templates.TemplateResponse("auth/home.html", {"request": request})

@app.get("/password-reset", response_class=HTMLResponse)
async def password_reset(request: Request):
    return templates.TemplateResponse("auth/password_reset.html", {"request": request})

@app.post("/password-reset")
async def password_reset_post(request: Request, email: str = Form(...)):
    # Здесь логика восстановления пароля
    return templates.TemplateResponse("home.html", {"request": request})
>>>>>>> 5b226d76a19ca7ee0b6f398c970d0a3e1558c542
