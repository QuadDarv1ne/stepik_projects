from pymongo import MongoClient
from bson import ObjectId
import json
from datetime import datetime

# Подключение к базе данных MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["taskify"]
collection = db["tasks"]


def save_to_json():
    # Получаем все задачи из коллекции
    tasks = list(collection.find({}))
    for task in tasks:
        # Преобразуем _id в строку
        task["_id"] = str(task["_id"])
        # Преобразуем даты в формат ISO
        task["created_at"] = task["created_at"].isoformat() if task.get("created_at") else None
        task["updated_at"] = task["updated_at"].isoformat() if task.get("updated_at") else None
    # Сохраняем задачи в JSON-файл
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=4)


def load_from_json():
    try:
        # Читаем задачи из JSON-файла
        with open("tasks.json") as f:
            tasks = json.load(f)

        for task in tasks:
            # Преобразуем _id обратно в ObjectId
            task["_id"] = ObjectId(task["_id"])
            # Преобразуем даты из формата ISO
            if "created_at" in task and task["created_at"]:
                task["created_at"] = datetime.fromisoformat(task["created_at"])
            else:
                task["created_at"] = None
            if "updated_at" in task and task["updated_at"]:
                task["updated_at"] = datetime.fromisoformat(task["updated_at"])
            else:
                task["updated_at"] = None

            # Проверяем, существует ли уже задача в коллекции
            existing_task = collection.find_one({"_id": task["_id"]})
            if existing_task:
                # Обновляем существующую задачу, если она уже есть
                collection.update_one({"_id": task["_id"]}, {"$set": task})
                print(f"Обновлена задача: {task['_id']}")
            else:
                # Вставляем новую задачу, если её нет в коллекции
                collection.insert_one(task)
                print(f"Добавлена новая задача: {task['_id']}")

    except FileNotFoundError:
        print("Файл 'tasks.json' не найден.")
    except json.JSONDecodeError:
        print("Ошибка при декодировании JSON файла.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


# Вызов функции для загрузки данных из JSON
load_from_json()
