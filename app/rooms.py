from flask import render_template, redirect, url_for, flash, request, session
from models import *


def view_rooms(app):
    @app.route("/view_rooms", methods=["GET"])
    def view_rooms():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        rooms = Room.query.all()
        return render_template("view_rooms.html", rooms=rooms)


def add_room(app):
    @app.route("/rooms/add", methods=["GET", "POST"])
    def add_room():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        if request.method == "POST":
            name = request.form['name']
            capacity = request.form['capacity']
            status = request.form['status']

            new_room = Room(
                name=name,
                capacity=capacity,
                status=status
            )

            try:
                db.session.add(new_room)
                db.session.commit()
                flash('Комната успешно добавлена!', 'success')
                return redirect(url_for('view_rooms'))
            except Exception as e:
                db.session.rollback()
                flash('Ошибка при добавлении комнаты. Попробуйте снова.', 'danger')
                return redirect(url_for('add_room'))

        return render_template("add_room.html")


def edit_room(app):
    @app.route("/rooms/edit/<int:room_id>", methods=["GET", "POST"])
    def edit_room(room_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        room = Room.query.get_or_404(room_id)

        if request.method == "POST":
            room.name = request.form['name']
            room.capacity = request.form['capacity']
            room.status = request.form['status']

            try:
                db.session.commit()
                flash('Комната успешно обновлена!', 'success')
                return redirect(url_for('view_rooms'))
            except Exception as e:
                db.session.rollback()
                flash('Ошибка при обновлении комнаты. Попробуйте снова.', 'danger')
                return redirect(url_for('edit_room', room_id=room_id))

        return render_template("edit_room.html", room=room)


def delete_room(app):
    @app.route("/rooms/delete/<int:room_id>", methods=["POST"])
    def delete_room(room_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        room = Room.query.get_or_404(room_id)

        try:
            db.session.delete(room)
            db.session.commit()
            flash('Комната успешно удалена!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при удалении комнаты. Попробуйте снова.', 'danger')

        return redirect(url_for('view_rooms'))
