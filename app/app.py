from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness_club.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'oxxxymiron'

db.init_app(app)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Пользователь с таким именем уже существует!', 'danger')
            return redirect(url_for('register'))

        email_user = User.query.filter_by(email=email).first()
        if email_user:
            flash('Пользователь с таким email уже существует!', 'danger')
            return redirect(url_for('register'))

        # Создание нового пользователя
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Ваш аккаунт был успешно создан! Теперь вы можете войти.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при регистрации. Попробуйте снова.', 'danger')
            return redirect(url_for('register'))

    return render_template("register.html")


# Маршрут для входа
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Поиск пользователя по имени
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.user_id  # Сохраняем идентификатор пользователя в сессии
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('dashboard'))  # Например, на главную страницу
        else:
            flash('Неверное имя пользователя или пароль!', 'danger')
            return redirect(url_for('login'))

    return render_template("login.html")


# Маршрут для выхода
@app.route("/logout")
def logout():
    session.pop('user_id', None)  # Удаление пользователя из сессии
    flash('Вы вышли из системы!', 'info')
    return redirect(url_for('login'))


# Маршрут для панели пользователя (например, главная страница)
@app.route("/")
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Если нет сессии, перенаправляем на страницу входа
    user = db.session.get(User, session['user_id'])
    return render_template("dashboard.html", user=user)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
