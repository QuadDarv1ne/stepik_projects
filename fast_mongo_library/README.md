# Fast Mongo Library

## Описание web-приложения:
**Fast Mongo Library** — это современное веб-приложение для управления библиотекой книг, разработанное с использованием фреймворка FastAPI и базы данных MongoDB.

Проект демонстрирует использование асинхронного программирования в Python для создания высокопроизводительных веб-сервисов и взаимодействия с MongoDB, используя ODM (Object Document Mapper).

### 🖥️ Основные возможности:

**1️⃣ CRUD Операции:** Позволяет создавать, читать, обновлять и удалять записи о книгах.

**2️⃣ Валидация данных:** Использует Pydantic для проверки и валидации данных запросов и ответов.

**3️⃣ Асинхронность:** Реализован асинхронный подход к обработке запросов для повышения производительности и масштабируемости.

**4️⃣ Документация API:** Автоматически генерирует документацию для API с помощью Swagger и ReDoc, доступную по URL /docs и /redoc.

**5️⃣ Тестирование:** Включает набор тестов для проверки корректности работы API и обработки различных сценариев запросов.

### 🛠 Стек технологий:

**FastAPI:** Современный, быстрый (высокопроизводительный) веб-фреймворк для создания API с Python 3.6+.

**MongoDB:** Документо-ориентированная база данных NoSQL.

**Pydantic:** Библиотека для валидации данных и работы с данными.

**Uvicorn:** Быстрый ASGI сервер для разработки и развертывания асинхронных веб-приложений.

**pytest:** Фреймворк для тестирования с поддержкой асинхронного программирования.

### 📖 Структура проекта:
```
fast_mongo_library/
│
├── app/
│   ├── __init__.py
│   ├── main.py            ⬅️ основной файл проекта
│   ├── crud.py
│   ├── models.py          ⬅️ модели базы данных
│   ├── schemas.py         ⬅️ схема базы данных
│   └── database.py        ⬅️ база данных
│
├── data/
│   └── books.json         ⬅️ словарь с книгами
│
├── .env
├── .gitignore             ⬅️ файл для игнорируемых файлов и папок в git
├── generate_secretkey.py  ⬅️ генерация секретного ключа
├── load_data.py           ⬅️ загрузка данных в базу данных
├── requirements.txt       ⬅️ установка необходимых библиотек
├── README.md              ⬅️ описание проекта
└── LICENSE                ⬅️ файл лицензии       
```

### Запуск проекта:
**cmd:** uvicorn app.main:app --reload

Если не работает на 8000 порту, то можно запустить на 8080 или 7000:

**cmd:** uvicorn app.main:app --port 8080

**cmd:** python -m uvicorn app.main:app --port 7000

### Установка зависимостей:
**cmd:** pip install fastapi uvicorn sqlalchemy sqlite3

### Взаимодействие с API:
**A) Получить список всех книг:** GET /books/

**B) Получить информацию о книге по ID:** GET /books/{id}

**C) Добавить новую книгу:** POST /books/

**D) Обновить информацию о книге:** PUT /books/{id}

**E) Удалить книгу:** DELETE /books/{id}

### 🛡 Лицензия
Этот проект лицензирован под лицензией MIT. Подробности смотрите в файле LICENSE.

### 💡 Идеи для улучшений
Новые идеи ...

### Примечания

- Убедитесь, что MongoDB запущен и доступен по указанному адресу.
- Проверьте, что все переменные окружения установлены правильно в `.env`.
- Запуск сервера и тестов должен происходить в активированном виртуальном окружении.


#### 💼 Автор: Дуплей Максим Игоревич
#### 📲 Telegram: @QuadD4rv1n7
#### 📅 Дата: 18.08.2024