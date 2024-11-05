import json
from app.database import engine
from app.models import Base, Category, Genre, Role, User
from sqlalchemy.orm import Session
from app.database import SessionLocal
from sqlalchemy.exc import IntegrityError

# Создаем таблицы
Base.metadata.create_all(bind=engine)

def populate_categories():
    with open("static/categories.json") as f:
        categories = json.load(f)

    db: Session = SessionLocal()
    try:
        for category in categories:
            db_category = Category(name=category["name"])
            db.add(db_category)
        db.commit()
    finally:
        db.close()


def populate_genres():
    with open("static/genres.json") as f:
        genres = json.load(f)

    db: Session = SessionLocal()
    try:
        for genre in genres:
            db_genre = Genre(name=genre["name"])
            db.add(db_genre)
        db.commit()
    finally:
        db.close()


def populate_roles():
    with open("static/roles.json") as f:
        roles = json.load(f)

    db: Session = SessionLocal()
    try:
        for role in roles:
            # Проверка, чтобы избежать дублирования
            existing_role = db.query(Role).filter_by(name=role["name"]).first()
            if existing_role:
                print(f"Роль '{role['name']}' уже существует. Пропускаем.")
                continue

            db_role = Role(name=role["name"])
            db.add(db_role)
        db.commit()
    finally:
        db.close()


def populate_accounts():
    with open("static/accounts.json") as f:
        accounts = json.load(f)

    db: Session = SessionLocal()
    try:
        for account in accounts:
            # Проверка, чтобы избежать дублирования
            existing_user = db.query(User).filter_by(username=account["username"]).first()
            if existing_user:
                print(f"Аккаунт '{account['username']}' уже существует. Пропускаем.")
                continue

            # Найти роль по имени
            role = db.query(Role).filter_by(name=account["role"]).first()
            if not role:
                print(f"Роль '{account['role']}' не найдена для пользователя '{account['username']}'. Пропускаем.")
                continue

            db_user = User(
                username=account["username"],
                email=account["email"],
                role_id=role.id  # Привязать роль по ID
            )
            db_user.set_password(account["password"])  # Установить хэшированный пароль
            db.add(db_user)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    populate_categories()
    populate_genres()
    populate_roles()
    populate_accounts()

