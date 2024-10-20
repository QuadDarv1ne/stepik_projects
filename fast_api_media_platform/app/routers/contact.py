# app/routes/contact.py
from flask import render_template, request, redirect, url_for, flash
from flask_mail import Message
from . import app, mail

@app.route('/send-message', methods=['POST'])
def send_message():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    msg = Message(subject='Новое сообщение от ' + name,
                  recipients=['recipient@example.com'],  # Укажите email, куда будут отправляться сообщения
                  body=f'Имя: {name}\nEmail: {email}\nСообщение:\n{message}')
    
    try:
        mail.send(msg)
        flash('Сообщение успешно отправлено!', 'success')
    except Exception as e:
        flash('Произошла ошибка при отправке сообщения. Пожалуйста, попробуйте позже.', 'danger')
    
    return redirect(url_for('contact'))  # Перенаправление на страницу контактов
