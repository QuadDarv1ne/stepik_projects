import json
import asyncio
from app.database import collection

async def load_initial_data():
    with open('data/books.json', 'r', encoding='utf-8') as file:
        books = json.load(file)
        await collection.insert_many(books)

if __name__ == "__main__":
    asyncio.run(load_initial_data())
