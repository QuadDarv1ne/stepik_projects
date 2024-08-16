from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["taskify"]
collection = db["tasks"]

# Обновление всех документов в коллекции, добавление значений по умолчанию для отсутствующих полей
collection.update_many(
    {"created_at": {"$exists": False}},
    {"$set": {"created_at": None}}
)

collection.update_many(
    {"updated_at": {"$exists": False}},
    {"$set": {"updated_at": None}}
)
