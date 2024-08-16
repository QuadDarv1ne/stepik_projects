import logging
from fastapi import FastAPI, Depends, HTTPException, Request, Form, File, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from starlette.requests import Request
from app.models import MediaFile
from starlette.responses import HTMLResponse

from app import models, crud
from app.database import engine, SessionLocal
from werkzeug.utils import secure_filename
import os

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
        music_file: UploadFile = File(...),
        cover_file: UploadFile = File(...),
        category_id: int = Form(...),
        genre_id: int = Form(...),
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
            file_name=music_filename,
            file_path=music_file_path,
            cover_image_path=cover_file_path,
            category_id=category_id,
            genre_id=genre_id
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

'''
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Максимальный размер файла 16MB
allowed_extensions = {'mp3', 'wav', 'jpg', 'png'}
'''