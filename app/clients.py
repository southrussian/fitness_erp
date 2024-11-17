from flask import render_template, redirect, url_for, flash, request, session
from models import *


def view_clients(app):
    @app.route("/view_clients", methods=["GET"])
    def view_clients():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        clients = Client.query.all()
        return render_template("view_clients.html", clients=clients)


def add_client(app):
    @app.route("/clients/add", methods=["GET", "POST"])
    def add_client():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        if request.method == "POST":
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            middle_name = request.form['middle_name']
            date_of_birth = request.form['date_of_birth']
            phone_number = request.form['phone_number']
            email = request.form['email']
            address = request.form['address']
            membership_id = request.form['membership_id']
            status = request.form['status']

            new_client = Client(
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
                date_of_birth=date_of_birth,
                phone_number=phone_number,
                email=email,
                address=address,
                membership_id=membership_id,
                status=status
            )

            try:
                db.session.add(new_client)
                db.session.commit()
                flash('Клиент успешно добавлен!', 'success')
                return redirect(url_for('view_clients'))
            except Exception as e:
                db.session.rollback()
                flash('Ошибка при добавлении клиента. Попробуйте снова.', 'danger')
                return redirect(url_for('add_client'))

        memberships = Membership.query.all()
        return render_template("add_client.html", memberships=memberships)

def edit_client(app):
    @app.route("/clients/edit/<int:client_id>", methods=["GET", "POST"])
    def edit_client(client_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        client = Client.query.get_or_404(client_id)

        if request.method == "POST":
            client.first_name = request.form['first_name']
            client.last_name = request.form['last_name']
            client.middle_name = request.form['middle_name']
            client.date_of_birth = request.form['date_of_birth']
            client.phone_number = request.form['phone_number']
            client.email = request.form['email']
            client.address = request.form['address']
            client.membership_id = request.form['membership_id']
            client.status = request.form['status']

            try:
                db.session.commit()
                flash('Клиент успешно обновлен!', 'success')
                return redirect(url_for('view_clients'))
            except Exception as e:
                db.session.rollback()
                flash('Ошибка при обновлении клиента. Попробуйте снова.', 'danger')
                return redirect(url_for('edit_client', client_id=client_id))

        memberships = Membership.query.all()
        return render_template("edit_client.html", client=client, memberships=memberships)


def delete_client(app):
    @app.route("/clients/delete/<int:client_id>", methods=["POST"])
    def delete_client(client_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        client = Client.query.get_or_404(client_id)

        try:
            db.session.delete(client)
            db.session.commit()
            flash('Клиент успешно удален!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при удалении клиента. Попробуйте снова.', 'danger')

        return redirect(url_for('view_clients'))


