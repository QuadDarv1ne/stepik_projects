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


from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models import User, Favorite
from app.schemas import FavoriteCreate, UserCreate, User

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


# Для работы с паролями
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 для авторизации
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Регистрация пользователя
@app.post("/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Вход пользователя
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Неправильный email или пароль")
    return {"access_token": user.username, "token_type": "bearer"}


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

'''
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Максимальный размер файла 16MB
allowed_extensions = {'mp3', 'wav', 'jpg', 'png'}
'''

@app.post("/favorites/", response_model=Favorite)
def add_favorite(favorite: FavoriteCreate, db: Session = Depends(get_db)):
    db_favorite = Favorite(user_id=favorite.user_id, music_id=favorite.music_id)
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite

@app.delete("/favorites/{favorite_id}")
def delete_favorite(favorite_id: int, db: Session = Depends(get_db)):
    favorite = db.query(Favorite).filter(Favorite.id == favorite_id).first()
    db.delete(favorite)
    db.commit()
    return {"detail": "Избранное удалено"}
