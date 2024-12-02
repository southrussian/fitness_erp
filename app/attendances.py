from flask import render_template, redirect, url_for, flash, request, session
from models import *


def view_attendance(app):
    @app.route("/view_attendance", methods=["GET"])
    def view_attendance():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        attendances = Attendance.query.all()
        return render_template("view_attendance.html", attendances=attendances)


def add_attendance(app):
    @app.route("/attendance/add", methods=["GET", "POST"])
    def add_attendance():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        if request.method == "POST":
            client_id = request.form['client_id']
            class_id = request.form['class_id']
            date = request.form['date']
            check_in_time = request.form['check_in_time']
            check_out_time = request.form['check_out_time']

            new_attendance = Attendance(
                client_id=client_id,
                class_id=class_id,
                date=date,
                check_in_time=check_in_time,
                check_out_time=check_out_time
            )

            try:
                db.session.add(new_attendance)
                db.session.commit()
                flash('Посещение успешно добавлено!', 'success')
                return redirect(url_for('view_attendance'))
            except Exception as e:
                db.session.rollback()
                flash('Ошибка при добавлении посещения. Попробуйте снова.', 'danger')
                return redirect(url_for('add_attendance'))

        clients = Client.query.all()
        classes = Class.query.all()
        return render_template("add_attendance.html", clients=clients, classes=classes)


def edit_attendance(app):
    @app.route("/attendance/edit/<int:attendance_id>", methods=["GET", "POST"])
    def edit_attendance(attendance_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        attendance = Attendance.query.get_or_404(attendance_id)

        if request.method == "POST":
            attendance.client_id = request.form['client_id']
            attendance.class_id = request.form['class_id']
            attendance.date = request.form['date']
            attendance.check_in_time = request.form['check_in_time']
            attendance.check_out_time = request.form['check_out_time']

            try:
                db.session.commit()
                flash('Посещение успешно обновлено!', 'success')
                return redirect(url_for('view_attendance'))
            except Exception as e:
                db.session.rollback()
                flash('Ошибка при обновлении посещения. Попробуйте снова.', 'danger')
                return redirect(url_for('edit_attendance', attendance_id=attendance_id))

        clients = Client.query.all()
        classes = Class.query.all()
        return render_template("edit_attendance.html", attendance=attendance, clients=clients, classes=classes)


def delete_attendance(app):
    @app.route("/attendance/delete/<int:attendance_id>", methods=["POST"])
    def delete_attendance(attendance_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        attendance = Attendance.query.get_or_404(attendance_id)

        try:
            db.session.delete(attendance)
            db.session.commit()
            flash('Посещение успешно удалено!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при удалении посещения. Попробуйте снова.', 'danger')

        return redirect(url_for('view_attendance'))
