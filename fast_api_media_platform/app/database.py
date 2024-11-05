from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# Настройка URL базы данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./media_platform.db"

# Создание объекта движка базы данных
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # для SQLite, чтобы разрешить множественные потоки
)

# Настройка сессии для взаимодействия с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

def init_db():
    """Инициализация базы данных, создание всех таблиц."""
    Base.metadata.create_all(bind=engine)

@contextmanager
def get_db_session():
    """Контекстный менеджер для управления сессией базы данных."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
