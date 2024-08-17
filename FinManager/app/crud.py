from pymongo import MongoClient
from typing import List, Optional
from bson import ObjectId
from models import User, Transaction, Budget

# Подключение к базе данных MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['finmanage']

# Функция для преобразования документа MongoDB в объект Pydantic
def parse_user(user_doc) -> Optional[User]:
    if user_doc:
        user_doc['id'] = str(user_doc['_id'])
        return User(**user_doc)
    return None

# Функция для получения пользователя по email
async def get_user_by_email(email: str) -> Optional[User]:
    user_doc = db['users'].find_one({"email": email})
    return parse_user(user_doc)

# Функция для получения пользователя по username
async def get_user_by_username(username: str) -> Optional[User]:
    user_doc = db['users'].find_one({"username": username})
    return parse_user(user_doc)

# Функция для создания пользователя
async def create_user(user: User):
    # Преобразование Pydantic модели в словарь и удаление id, чтобы MongoDB назначил его автоматически
    user_dict = user.dict(exclude={"id"})
    db['users'].insert_one(user_dict)

# Функция для получения транзакций по user_id
async def get_transactions(user_id: str) -> List[Transaction]:
    transactions = db['transactions'].find({"user_id": user_id})
    return [Transaction(**txn) for txn in transactions]

# Функция для создания транзакции
async def create_transaction(transaction: Transaction):
    transaction_dict = transaction.dict(exclude={"id"})
    db['transactions'].insert_one(transaction_dict)

# Функция для получения бюджетов по user_id
async def get_budgets(user_id: str) -> List[Budget]:
    budgets = db['budgets'].find({"user_id": user_id})
    return [Budget(**budget) for budget in budgets]

# Функция для создания бюджета
async def create_budget(budget: Budget):
    budget_dict = budget.dict(exclude={"id"})
    db['budgets'].insert_one(budget_dict)
