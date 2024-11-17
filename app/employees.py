from flask import render_template, redirect, url_for, flash, request, session
from models import *


def view_employees(app):
    @app.route("/view_employees", methods=["GET"])
    def view_employees():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        employees = Employee.query.all()
        return render_template("view_employees.html", employees=employees)


def add_employees(app):
    @app.route("/employees/add", methods=["GET", "POST"])
    def add_employee():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        if request.method == "POST":
            user_id = request.form['user_id']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            middle_name = request.form['middle_name']
            position = request.form['position']
            phone_number = request.form['phone_number']
            email = request.form['email']
            salary = request.form['salary']
            status = request.form['status']

            new_employee = Employee(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
                position=position,
                phone_number=phone_number,
                email=email,
                salary=salary,
                status=status
            )

            try:
                db.session.add(new_employee)
                db.session.commit()
                flash('Сотрудник успешно добавлен!', 'success')
                return redirect(url_for('view_employees'))
            except Exception as e:
                db.session.rollback()
                flash('Ошибка при добавлении сотрудника. Попробуйте снова.', 'danger')
                return redirect(url_for('add_employee'))

        users = User.query.all()
        return render_template("add_employee.html", users=users)


def edit_employees(app):
    @app.route("/employees/edit/<int:employee_id>", methods=["GET", "POST"])
    def edit_employee(employee_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        employee = Employee.query.get_or_404(employee_id)

        if request.method == "POST":
            employee.user_id = request.form['user_id']
            employee.first_name = request.form['first_name']
            employee.last_name = request.form['last_name']
            employee.middle_name = request.form['middle_name']
            employee.position = request.form['position']
            employee.phone_number = request.form['phone_number']
            employee.email = request.form['email']
            employee.salary = request.form['salary']
            employee.status = request.form['status']

            try:
                db.session.commit()
                flash('Сотрудник успешно обновлен!', 'success')
                return redirect(url_for('view_employees'))
            except Exception as e:
                db.session.rollback()
                flash('Ошибка при обновлении сотрудника. Попробуйте снова.', 'danger')
                return redirect(url_for('edit_employee', employee_id=employee_id))

        users = User.query.all()
        return render_template("edit_employee.html", employee=employee, users=users)


def delete_employees(app):
    @app.route("/employees/delete/<int:employee_id>", methods=["POST"])
    def delete_employee(employee_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        employee = Employee.query.get_or_404(employee_id)

        try:
            db.session.delete(employee)
            db.session.commit()
            flash('Сотрудник успешно удален!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при удалении сотрудника. Попробуйте снова.', 'danger')

        return redirect(url_for('view_employees'))
