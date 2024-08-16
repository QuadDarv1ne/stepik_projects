from bson import ObjectId
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from database import db

tasks_collection: Collection = db.tasks

def create_task(task: dict):
    try:
        result = tasks_collection.insert_one(task)
        return str(result.inserted_id)
    except PyMongoError as e:
        print(f"Ошибка при создании задачи: {e}")
        return None

def get_task(task_id: str):
    try:
        task = tasks_collection.find_one({"_id": ObjectId(task_id)})
        if task:
            task["_id"] = str(task["_id"])
        return task
    except PyMongoError as e:
        print(f"Ошибка при получении задачи: {e}")
        return None

def update_task(task_id: str, task: dict):
    try:
        result = tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": task})
        return result.modified_count > 0
    except PyMongoError as e:
        print(f"Ошибка при обновлении задачи: {e}")
        return False

def delete_task(task_id: str):
    try:
        result = tasks_collection.delete_one({"_id": ObjectId(task_id)})
        return result.deleted_count > 0
    except PyMongoError as e:
        print(f"Ошибка при удалении задачи: {e}")
        return False

def get_all_tasks():
    try:
        tasks = tasks_collection.find()
        return [{**task, "_id": str(task["_id"])} for task in tasks]
    except PyMongoError as e:
        print(f"Ошибка при получении всех задач: {e}")
        return []
