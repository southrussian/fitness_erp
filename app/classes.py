from flask import render_template, redirect, url_for, flash, request, session
from models import *


def view_classes(app):
    @app.route("/view_classes", methods=["GET"])
    def view_classes():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        classes = Class.query.all()
        return render_template("view_classes.html", classes=classes)


def add_class(app):
    @app.route("/classes/add", methods=["GET", "POST"])
    def add_class():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        if request.method == "POST":
            name = request.form['name']
            description = request.form['description']
            employee_id = request.form['employee_id']
            schedule_id = request.form['schedule_id']
            duration = request.form['duration']
            max_participants = request.form['max_participants']

            new_class = Class(
                name=name,
                description=description,
                employee_id=employee_id,
                schedule_id=schedule_id,
                duration=duration,
                max_participants=max_participants
            )

            try:
                db.session.add(new_class)
                db.session.commit()
                flash('Занятие успешно добавлено!', 'success')
                return redirect(url_for('view_classes'))
            except Exception as e:
                db.session.rollback()
                flash('Ошибка при добавлении занятия. Попробуйте снова.', 'danger')
                return redirect(url_for('add_class'))

        employees = Employee.query.all()
        schedules = Schedule.query.all()
        return render_template("add_class.html", employees=employees, schedules=schedules)


def edit_class(app):
    @app.route("/classes/edit/<int:class_id>", methods=["GET", "POST"])
    def edit_class(class_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        class_info = Class.query.get_or_404(class_id)

        if request.method == "POST":
            class_info.name = request.form['name']
            class_info.description = request.form['description']
            class_info.employee_id = request.form['employee_id']
            class_info.schedule_id = request.form['schedule_id']
            class_info.duration = request.form['duration']
            class_info.max_participants = request.form['max_participants']

            try:
                db.session.commit()
                flash('Занятие успешно обновлено!', 'success')
                return redirect(url_for('view_classes'))
            except Exception as e:
                db.session.rollback()
                flash('Ошибка при обновлении занятия. Попробуйте снова.', 'danger')
                return redirect(url_for('edit_class', class_id=class_id))

        employees = Employee.query.all()
        schedules = Schedule.query.all()
        return render_template("edit_class.html", class_info=class_info, employees=employees, schedules=schedules)


def delete_class(app):
    @app.route("/classes/delete/<int:class_id>", methods=["POST"])
    def delete_class(class_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        class_info = Class.query.get_or_404(class_id)

        try:
            db.session.delete(class_info)
            db.session.commit()
            flash('Занятие успешно удалено!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при удалении занятия. Попробуйте снова.', 'danger')

        return redirect(url_for('view_classes'))
