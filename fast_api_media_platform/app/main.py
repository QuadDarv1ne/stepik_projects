import logging
import os
from fastapi import FastAPI, Depends, HTTPException, Request, Form, File, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app import models, crud
from app.database import engine, SessionLocal
from werkzeug.utils import secure_filename
from app.routers import auth

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Инициализация FastAPI
app = FastAPI()
app.include_router(auth.router)

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
        response.headers["Cache-Control"] = "public, max-age=600"  # Кэшируем на 10 минут
    return response

@app.get("/")
async def read_root(request: Request, db: Session = Depends(get_db)):
    return await render_template(request, "index.html", db)

@app.get("/upload")
async def upload_form(request: Request, db: Session = Depends(get_db)):
    return await render_template(request, "upload.html", db)

@app.post("/upload")
async def upload_file(
        name_music: str = Form(...),
        music_file: UploadFile = File(...),
        cover_file: UploadFile = File(...),
        category_id: int = Form(...),
        genre_id: int = Form(...),
        youtube_url: str = Form(None),
        rutube_url: str = Form(None),
        plvideo_url: str = Form(None),
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

        # Сохранение файлов
        await save_file(music_file, os.path.join(music_dir, music_filename))
        await save_file(cover_file, os.path.join(cover_dir, cover_filename))

        # Добавление записи в базу данных
        crud.create_media_file(
            db=db,
            name_music=name_music,
            file_name=music_filename,
            file_path=os.path.join(music_dir, music_filename),
            cover_image_path=os.path.join(cover_dir, cover_filename),
            category_id=category_id,
            genre_id=genre_id,
            youtube_url=youtube_url,
            rutube_url=rutube_url,
            plvideo_url=plvideo_url
        )
        return RedirectResponse("/", status_code=303)
    except SQLAlchemyError as e:
        log_and_raise(e, "Ошибка базы данных")
    except Exception as e:
        log_and_raise(e, "Ошибка загрузки файла")

@app.get("/create-category")
async def create_category_form(request: Request):
    return templates.TemplateResponse("create_category.html", {"request": request})

@app.post("/create-category")
async def create_category(name: str = Form(...), db: Session = Depends(get_db)):
    return await handle_category_operation(name, crud.create_category, db)

@app.get("/create-genre")
async def create_genre_form(request: Request):
    return templates.TemplateResponse("create_genre.html", {"request": request})

@app.post("/create-genre")
async def create_genre(name: str = Form(...), db: Session = Depends(get_db)):
    return await handle_category_operation(name, crud.create_genre, db)

@app.get("/media/{media_id}")
async def read_media(request: Request, media_id: int, db: Session = Depends(get_db)):
    media_file = crud.get_media_file_by_id(db, media_id)
    if media_file is None:
        raise HTTPException(status_code=404, detail="Медиа файл не найден")
    return templates.TemplateResponse("media_detail.html", {"request": request, "media_file": media_file})

@app.on_event("shutdown")
def cleanup_temp_files():
    temp_dir = '/path/to/temp/dir'
    for filename in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, filename)
        if os.path.isfile(file_path):
            try:
                os.unlink(file_path)
            except Exception as e:
                logger.error(f"Ошибка при удалении файла: {e}")

@app.get("/edit-media/{media_id}")
async def edit_media_form(request: Request, media_id: int, db: Session = Depends(get_db)):
    media_file = crud.get_media_file_by_id(db, media_id)
    if media_file is None:
        raise HTTPException(status_code=404, detail="Медиа файл не найден")
    categories = crud.get_categories(db)
    genres = crud.get_genres(db)
    return templates.TemplateResponse("edit_media.html", {"request": request, "media_file": media_file, "categories": categories, "genres": genres})

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
    media_file = crud.get_media_file_by_id(db, media_id)
    if media_file is None:
        raise HTTPException(status_code=404, detail="Медиа файл не найден")

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
    return RedirectResponse(f"/media/{media_id}", status_code=303)

@app.get("/register")
async def register_form(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})

@app.post("/register")
async def register(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if crud.get_user(db, username):
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    crud.create_user(db=db, username=username, password=password)
    return templates.TemplateResponse("auth/login.html", {"request": Request, "message": "Регистрация прошла успешно, теперь вы можете войти."})

@app.get("/login")
async def login_form(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Неправильное имя пользователя или пароль")
    return {"access_token": user.username, "token_type": "bearer"}

# Вспомогательные функции
async def render_template(request: Request, template_name: str, db: Session):
    try:
        media_files = crud.get_media_files(db)
        return templates.TemplateResponse(template_name, {"request": request, "media_files": media_files})
    except SQLAlchemyError as e:
        log_and_raise(e, "Ошибка базы данных")

async def save_file(upload_file: UploadFile, file_path: str):
    with open(file_path, "wb") as f:
        f.write(await upload_file.read())

def log_and_raise(exception, message):
    logger.error(f"{message}: {exception}")
    raise HTTPException(status_code=500, detail=message)

async def handle_category_operation(name: str, create_function, db: Session):
    try:
        create_function(db=db, name=name)
        return RedirectResponse("/", status_code=303)
    except SQLAlchemyError as e:
        log_and_raise(e, "Ошибка базы данных")
