# Это пустой файл, который делает папку 'app' пакетом Python
# app/__init__.py
from flask import Flask
from flask_mail import Mail

app = Flask(__name__)

# Настройка конфигурации для Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.example.com'  # Укажите ваш SMTP-сервер
app.config['MAIL_PORT'] = 587  # Обычно 587 для TLS
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'  # Ваш email
app.config['MAIL_PASSWORD'] = 'your_password'  # Ваш пароль
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'

mail = Mail(app)
