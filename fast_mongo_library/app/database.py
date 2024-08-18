from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

MONGO_DETAILS = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.library_db
collection = database.books
