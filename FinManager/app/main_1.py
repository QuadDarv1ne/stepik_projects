# Тестирование функции
from FinManager.app.auth import get_password_hash, verify_password

password = "1234567"
hashed_password = get_password_hash(password)
print("Hashed password:", hashed_password)

# Проверка правильности пароля
print("Password match:", verify_password(password, hashed_password))
