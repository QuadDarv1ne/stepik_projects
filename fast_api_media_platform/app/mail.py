from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

# Конфигурация для отправки электронной почты
conf = ConnectionConfig(
    MAIL_USERNAME="your_email@example.com",
    MAIL_PASSWORD="your_email_password",
    MAIL_FROM="your_email@example.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.example.com",
    MAIL_STARTTLS=True,  # Замените MAIL_TLS на MAIL_STARTTLS
    MAIL_SSL_TLS=False,   # Замените MAIL_SSL на MAIL_SSL_TLS
    USE_CREDENTIALS=True,
)

async def send_reset_email(email: str, token: str):
    message = MessageSchema(
        subject="Сброс пароля",
        recipients=[email],
        body=f"Вот ваша ссылка для сброса пароля: http://localhost:8000/reset/{token}",
        subtype="text",
    )

    fm = FastMail(conf)
    await fm.send_message(message)
