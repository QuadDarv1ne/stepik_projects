from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import RegistrationForm, LoginForm
from .models import User, Favorite
from . import db

auth = Blueprint('auth', __name__)

# Регистрация
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Ваш аккаунт создан! Теперь вы можете войти.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

# Вход
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.profile'))  # Замените на ваш маршрут
        flash('Неправильный email или пароль', 'danger')
    return render_template('login.html', form=form)

# Выход
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))  # Замените на ваш маршрут
