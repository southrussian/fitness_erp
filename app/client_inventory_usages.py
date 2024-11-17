from flask import render_template, redirect, url_for, flash, request, session
from models import *


def view_client_inventory_usage(app):
    @app.route("/view_client_inventory_usage", methods=["GET"])
    def view_client_inventory_usage():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        usages = ClientInventoryUsage.query.all()
        return render_template("view_client_inventory_usage.html", usages=usages)


def add_client_inventory_usage(app):
    @app.route("/client_inventory_usage/add", methods=["GET", "POST"])
    def add_client_inventory_usage():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        if request.method == "POST":
            client_id = request.form['client_id']
            inventory_id = request.form['inventory_id']
            date = request.form['date']
            start_time = request.form['start_time']
            end_time = request.form['end_time']

            new_usage = ClientInventoryUsage(
                client_id=client_id,
                inventory_id=inventory_id,
                date=date,
                start_time=start_time,
                end_time=end_time
            )

            try:
                db.session.add(new_usage)
                db.session.commit()
                flash('Использование инвентаря успешно добавлено!', 'success')
                return redirect(url_for('view_client_inventory_usage'))
            except Exception as e:
                db.session.rollback()
                flash('Ошибка при добавлении использования инвентаря. Попробуйте снова.', 'danger')
                return redirect(url_for('add_client_inventory_usage'))

        clients = Client.query.all()
        inventories = Inventory.query.all()
        return render_template("add_client_inventory_usage.html", clients=clients, inventories=inventories)


def edit_client_inventory_usage(app):
    @app.route("/client_inventory_usage/edit/<int:usage_id>", methods=["GET", "POST"])
    def edit_client_inventory_usage(usage_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        usage = ClientInventoryUsage.query.get_or_404(usage_id)

        if request.method == "POST":
            usage.client_id = request.form['client_id']
            usage.inventory_id = request.form['inventory_id']
            usage.date = request.form['date']
            usage.start_time = request.form['start_time']
            usage.end_time = request.form['end_time']

            try:
                db.session.commit()
                flash('Использование инвентаря успешно обновлено!', 'success')
                return redirect(url_for('view_client_inventory_usage'))
            except Exception as e:
                db.session.rollback()
                flash('Ошибка при обновлении использования инвентаря. Попробуйте снова.', 'danger')
                return redirect(url_for('edit_client_inventory_usage', usage_id=usage_id))

        clients = Client.query.all()
        inventories = Inventory.query.all()
        return render_template("edit_client_inventory_usage.html", usage=usage, clients=clients,
                               inventories=inventories)


def delete_client_inventory_usage(app):
    @app.route("/client_inventory_usage/delete/<int:usage_id>", methods=["POST"])
    def delete_client_inventory_usage(usage_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        usage = ClientInventoryUsage.query.get_or_404(usage_id)

        try:
            db.session.delete(usage)
            db.session.commit()
            flash('Использование инвентаря успешно удалено!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при удалении использования инвентаря. Попробуйте снова.', 'danger')

        return redirect(url_for('view_client_inventory_usage'))



