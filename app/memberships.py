from flask import render_template, redirect, url_for, flash, request, session
from models import *


def view_memberships(app):
    @app.route("/view_memberships", methods=["GET"])
    def view_memberships():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        memberships = Membership.query.all()
        return render_template("view_memberships.html", memberships=memberships)


def add_membership(app):
    @app.route("/memberships/add", methods=["GET", "POST"])
    def add_membership():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        if request.method == "POST":
            type = request.form['type']
            price = request.form['price']
            duration = request.form['duration']
            access_level = request.form['access_level']

            new_membership = Membership(type=type, price=price, duration=duration, access_level=access_level)

            try:
                db.session.add(new_membership)
                db.session.commit()
                flash('Членство успешно добавлено!', 'success')
                return redirect(url_for('view_memberships'))
            except Exception as e:
                db.session.rollback()
                flash('Ошибка при добавлении членства. Попробуйте снова.', 'danger')
                return redirect(url_for('add_membership'))

        return render_template("add_membership.html")

def edit_membership(app):
    @app.route("/memberships/edit/<int:membership_id>", methods=["GET", "POST"])
    def edit_membership(membership_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        membership = Membership.query.get_or_404(membership_id)

        if request.method == "POST":
            membership.type = request.form['type']
            membership.price = request.form['price']
            membership.duration = request.form['duration']
            membership.access_level = request.form['access_level']

            try:
                db.session.commit()
                flash('Членство успешно обновлено!', 'success')
                return redirect(url_for('view_memberships'))
            except Exception as e:
                db.session.rollback()
                flash('Ошибка при обновлении членства. Попробуйте снова.', 'danger')
                return redirect(url_for('edit_membership', membership_id=membership_id))

        return render_template("edit_membership.html", membership=membership)

def delete_membership(app):
    @app.route("/memberships/delete/<int:membership_id>", methods=["POST"])
    def delete_membership(membership_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        membership = Membership.query.get_or_404(membership_id)

        try:
            db.session.delete(membership)
            db.session.commit()
            flash('Членство успешно удалено!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при удалении членства. Попробуйте снова.', 'danger')

        return redirect(url_for('view_memberships'))
