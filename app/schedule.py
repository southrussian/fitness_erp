from flask import render_template, redirect, url_for, flash, request, session
from models import *


def view_schedules(app):
    @app.route("/view_schedules", methods=["GET"])
    def view_schedules():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        schedules = Schedule.query.all()
        return render_template("view_schedules.html", schedules=schedules)


def add_schedule(app):
    @app.route("/schedules/add", methods=["GET", "POST"])
    def add_schedule():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        if request.method == "POST":
            class_id = request.form['class_id']
            date = request.form['date']
            start_time = request.form['start_time']
            end_time = request.form['end_time']
            room_id = request.form['room_id']

            new_schedule = Schedule(
                class_id=class_id,
                date=date,
                start_time=start_time,
                end_time=end_time,
                room_id=room_id
            )

            try:
                db.session.add(new_schedule)
                db.session.commit()
                flash('Расписание успешно добавлено!', 'success')
                return redirect(url_for('view_schedules'))
            except Exception as e:
                db.session.rollback()
                flash('Ошибка при добавлении расписания. Попробуйте снова.', 'danger')
                return redirect(url_for('add_schedule'))

        classes = Class.query.all()
        rooms = Room.query.all()
        return render_template("add_schedule.html", classes=classes, rooms=rooms)


def edit_schedule(app):
    @app.route("/schedules/edit/<int:schedule_id>", methods=["GET", "POST"])
    def edit_schedule(schedule_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        schedule = Schedule.query.get_or_404(schedule_id)

        if request.method == "POST":
            schedule.class_id = request.form['class_id']
            schedule.date = request.form['date']
            schedule.start_time = request.form['start_time']
            schedule.end_time = request.form['end_time']
            schedule.room_id = request.form['room_id']

            try:
                db.session.commit()
                flash('Расписание успешно обновлено!', 'success')
                return redirect(url_for('view_schedules'))
            except Exception as e:
                db.session.rollback()
                flash('Ошибка при обновлении расписания. Попробуйте снова.', 'danger')
                return redirect(url_for('edit_schedule', schedule_id=schedule_id))

        classes = Class.query.all()
        rooms = Room.query.all()
        return render_template("edit_schedule.html", schedule=schedule, classes=classes, rooms=rooms)


def delete_schedule(app):
    @app.route("/schedules/delete/<int:schedule_id>", methods=["POST"])
    def delete_schedule(schedule_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        schedule = Schedule.query.get_or_404(schedule_id)

        try:
            db.session.delete(schedule)
            db.session.commit()
            flash('Расписание успешно удалено!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при удалении расписания. Попробуйте снова.', 'danger')

        return redirect(url_for('view_schedules'))

