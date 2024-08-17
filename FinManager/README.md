# Финансовый менеджмент на Fast API

## Описание web-приложения:


### 🖥️ Основные возможности:
1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 

### 🛠 Стек технологий:


### 📖 Структура проекта:
```
FinManager/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── auth.py
│   └── utils.py
│
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── register.html
│   ├── login.html
│   ├── transactions.html
│   ├── budgets.html
│   └── error.html
│
├── static/
│   └── style.css
│
├── .gitignore
├── requirements.txt
└── README.md
```

```
Загрузка данных в таблицы БД
python populate_data.py
```
### Установка:

**Клонируйте репозиторий:**

**cmd:** git clone https://github.com/ваш-репозиторий.git

### Запуск проекта:

**cmd:** uvicorn app.main:app --reload

**Если не работает на 8000 порту, то можно запустить на 8080 или 7000:**

**cmd:** python -m uvicorn app.main:app --port 8080

**cmd:** python -m uvicorn app.main:app --port 7000

### Установка зависимостей:

**cmd:** pip install fastapi uvicorn sqlalchemy sqlite3

### 🛡 Лицензия

Этот проект лицензирован под лицензией MIT. Подробности смотрите в файле LICENSE.

### 💡 Идеи для улучшений

Добавить аутентификацию и авторизацию для управления доступом к API.

Реализовать фильтрацию и поиск по различным параметрам книги.

Подключить базу данных для хранения данных о книгах вместо JSON-файла.

Разработать веб-интерфейс для удобного взаимодействия с библиотекой.

#### 💼 Автор: Дуплей Максим Игоревич
#### 📲 Telegram: @QuadD4rv1n7
#### 📅 Дата: 17.08.2024 