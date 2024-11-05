from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import models
from app import schemas
from app.models import MediaFile, User
from app.schemas import MediaFileCreate, UserCreate
import logging

# Настройка логирования
logger = logging.getLogger(__name__)

def get_media_files(db: Session) -> List[MediaFile]:
    """
    Получить все медиафайлы.

    :param db: Сессия базы данных.
    :return: Список всех медиафайлов.
    """
    return db.query(models.MediaFile).all()

def create_media_file(db: Session, media_file_data: MediaFileCreate) -> MediaFile:
    """
    Создать новый медиафайл с URL.

    :param db: Сессия базы данных.
    :param media_file_data: Данные для создания медиафайла.
    :return: Созданный медиафайл.
    """
    new_media_file = MediaFile(**media_file_data.dict())
    db.add(new_media_file)
    db.commit()
    db.refresh(new_media_file)
    logger.info(f"Создан новый медиафайл: {new_media_file.id}")
    return new_media_file

def get_media_file_by_id(db: Session, media_id: int) -> Optional[MediaFile]:
    """
    Получить медиафайл по его ID.

    :param db: Сессия базы данных.
    :param media_id: ID медиафайла.
    :return: Найденный медиафайл.
    :raises HTTPException: Если медиафайл не найден.
    """
    media_file = db.query(models.MediaFile).filter(models.MediaFile.id == media_id).first()
    if media_file is None:
        logger.error(f"Медиафайл не найден: {media_id}")
        raise HTTPException(status_code=404, detail="Медиа файл не найден")
    return media_file

def get_categories(db: Session) -> List[models.Category]:
    """
    Получить все категории.

    :param db: Сессия базы данных.
    :return: Список всех категорий.
    """
    return db.query(models.Category).all()

def get_genres(db: Session) -> List[models.Genre]:
    """
    Получить все жанры.

    :param db: Сессия базы данных.
    :return: Список всех жанров.
    """
    return db.query(models.Genre).all()

def create_category(db: Session, name: str) -> models.Category:
    """
    Создать новую категорию.

    :param db: Сессия базы данных.
    :param name: Название категории.
    :return: Созданная категория.
    """
    db_category = models.Category(name=name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    logger.info(f"Создана новая категория: {db_category.id}")
    return db_category

def create_genre(db: Session, name: str) -> models.Genre:
    """
    Создать новый жанр.

    :param db: Сессия базы данных.
    :param name: Название жанра.
    :return: Созданный жанр.
    """
    db_genre = models.Genre(name=name)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    logger.info(f"Создан новый жанр: {db_genre.id}")
    return db_genre

def update_media_file(db: Session, media_id: int, media_file_data: MediaFileCreate) -> MediaFile:
    """
    Обновить существующий медиафайл.

    :param db: Сессия базы данных.
    :param media_id: ID медиафайла для обновления.
    :param media_file_data: Новые данные медиафайла.
    :return: Обновленный медиафайл.
    """
    media_file = get_media_file_by_id(db, media_id)
    for field, value in media_file_data.dict().items():
        setattr(media_file, field, value)

    db.commit()
    db.refresh(media_file)
    logger.info(f"Обновлен медиафайл: {media_file.id}")
    return media_file

def search_media_files(db: Session, query: Optional[str], category_id: Optional[int], genre_id: Optional[int]) -> List[MediaFile]:
    """
    Поиск медиафайлов по критериям.

    :param db: Сессия базы данных.
    :param query: Поисковый запрос по имени музыки.
    :param category_id: ID категории для фильтрации.
    :param genre_id: ID жанра для фильтрации.
    :return: Список найденных медиафайлов.
    """
    query_result = db.query(MediaFile)

    if query:
        query_result = query_result.filter(MediaFile.name_music.ilike(f"%{query}%"))

    if category_id is not None:
        query_result = query_result.filter(MediaFile.category_id == category_id)

    if genre_id is not None:
        query_result = query_result.filter(MediaFile.genre_id == genre_id)

    logger.info(f"Поиск медиафайлов с запросом: {query}, категория: {category_id}, жанр: {genre_id}")
    return query_result.all()

def create_user(db: Session, user: UserCreate) -> User:
    """
    Создать нового пользователя с установкой значений по умолчанию.

    :param db: Сессия базы данных.
    :param user: Данные для создания пользователя.
    :return: Созданный пользователь.
    :raises ValueError: Если пользователь с таким именем или email уже существует.
    """
    # Проверка на существование пользователя
    existing_user = db.query(User).filter(
        (User.username == user.username) | 
        (User.email == user.email)
    ).first()
    
    if existing_user:
        logger.warning(f"Пользователь с именем {user.username} или email {user.email} уже существует.")
        raise ValueError("Пользователь с таким именем или адресом электронной почты уже существует.")

    # Создание нового пользователя
    db_user = User(
        username=user.username,
        email=user.email,
        profile_image_path='default_profile.png',  # Установить изображение профиля по умолчанию
        role_id=1,  # Установить роль по умолчанию (например, роль пользователя)
        is_active=True  # Активен по умолчанию
    )
    
    db_user.set_password(user.password)  # Установить хэшированный пароль

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(f"Создан новый пользователь: {db_user.id}")
    except Exception as e:
        db.rollback()  # Откатить изменения в случае ошибки
        logger.error(f"Ошибка при создании пользователя: {e}")
        raise

    return db_user

def update_user_profile(db: Session, user_id: int, username: str, email: str, profile_image_path: Optional[str] = None) -> Optional[models.User]:
    """
    Обновить профиль пользователя.

    :param db: Сессия базы данных.
    :param user_id: ID пользователя для обновления.
    :param username: Новое имя пользователя.
    :param email: Новый email пользователя.
    :param profile_image_path: Новый путь к изображению профиля (по желанию).
    :return: Обновленный пользователь.
    :raises HTTPException: Если пользователь не найден.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        logger.error(f"Пользователь не найден: {user_id}")
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    user.username = username
    user.email = email
    if profile_image_path:
        user.profile_image_path = profile_image_path

    db.commit()
    db.refresh(user)
    logger.info(f"Обновлен профиль пользователя: {user.id}")
    return user

# Дополнительные функции CRUD
def get_user(db: Session, user_id: int) -> User:
    """
    Получить пользователя по его ID.

    :param db: Сессия базы данных.
    :param user_id: ID пользователя.
    :return: Найденный пользователь.
    """
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> User:
    """
    Получить пользователя по имени пользователя.

    :param db: Сессия базы данных.
    :param username: Имя пользователя.
    :return: Найденный пользователь.
    """
    return db.query(User).filter(User.username == username).first()

def get_all_users(db: Session) -> List[User]:
    """
    Получить всех пользователей.

    :param db: Сессия базы данных.
    :return: Список всех пользователей.
    """
    return db.query(User).all()

def delete_user(db: Session, user_id: int) -> None:
    """
    Удалить пользователя по его ID.

    :param db: Сессия базы данных.
    :param user_id: ID пользователя для удаления.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        logger.info(f"Удален пользователь: {user_id}")

def update_user(db: Session, user_id: int, user_data: UserCreate) -> User:
    """
    Обновить информацию о пользователе.

    :param db: Сессия базы данных.
    :param user_id: ID пользователя для обновления.
    :param user_data: Новые данные пользователя.
    :return: Обновленный пользователь.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        if user_data.username:
            db_user.username = user_data.username
        if user_data.email:
            db_user.email = user_data.email
        if user_data.password:
            db_user.set_password(user_data.password)  # Установка хэшированного пароля
        db.commit()
        db.refresh(db_user)
        logger.info(f"Обновлен пользователь: {user_id}")
        return db_user
    else:
        logger.error(f"Пользователь не найден для обновления: {user_id}")
        raise HTTPException(status_code=404, detail="Пользователь не найден")
