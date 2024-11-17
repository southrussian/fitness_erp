from flask import Flask, render_template, redirect, url_for, flash, request, session
from models import *

from user import register, login, logout
from memberships import view_memberships, add_membership, edit_membership, delete_membership
from clients import view_clients, add_client, edit_client, delete_client
from employees import view_employees, add_employees, edit_employees, delete_employees
from classes import view_classes, add_class, edit_class, delete_class
from schedule import view_schedules, add_schedule, edit_schedule, delete_schedule
from payments import view_payments, add_payment, edit_payment, delete_payment
from client_inventory_usages import (view_client_inventory_usage, add_client_inventory_usage,
                                     edit_client_inventory_usage, delete_client_inventory_usage)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness_club.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'oxxxymiron'

db.init_app(app)

register(app)
login(app)
logout(app)

view_memberships(app)
add_membership(app)
edit_membership(app)
delete_membership(app)

view_clients(app)
add_client(app)
edit_client(app)
delete_client(app)

view_employees(app)
add_employees(app)
edit_employees(app)
delete_employees(app)

view_classes(app)
add_class(app)
edit_class(app)
delete_class(app)

view_schedules(app)
add_schedule(app)
edit_schedule(app)
delete_schedule(app)

view_payments(app)
add_payment(app)
edit_payment(app)
delete_payment(app)

view_client_inventory_usage(app)
add_client_inventory_usage(app)
edit_client_inventory_usage(app)
delete_client_inventory_usage(app)


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
