from flask import render_template, redirect, url_for, flash, request, session
from models import *

def view_inventory(app):
    @app.route("/view_inventory", methods=["GET"])
    def view_inventory():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        inventories = Inventory.query.all()
        return render_template("view_inventory.html", inventories=inventories)

def add_inventory(app):
    @app.route("/inventory/add", methods=["GET", "POST"])
    def add_inventory():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        if request.method == "POST":
            name = request.form['name']
            quantity = request.form['quantity']
            status = request.form['status']

            new_inventory = Inventory(
                name=name,
                quantity=quantity,
                status=status
            )

            try:
                db.session.add(new_inventory)
                db.session.commit()
                flash('Инвентарь успешно добавлен!', 'success')
                return redirect(url_for('view_inventory'))
            except Exception as e:
                db.session.rollback()
                flash('Ошибка при добавлении инвентаря. Попробуйте снова.', 'danger')
                return redirect(url_for('add_inventory'))

        return render_template("add_inventory.html")

def edit_inventory(app):
    @app.route("/inventory/edit/<int:inventory_id>", methods=["GET", "POST"])
    def edit_inventory(inventory_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        inventory = Inventory.query.get_or_404(inventory_id)

        if request.method == "POST":
            inventory.name = request.form['name']
            inventory.quantity = request.form['quantity']
            inventory.status = request.form['status']

            try:
                db.session.commit()
                flash('Инвентарь успешно обновлен!', 'success')
                return redirect(url_for('view_inventory'))
            except Exception as e:
                db.session.rollback()
                flash('Ошибка при обновлении инвентаря. Попробуйте снова.', 'danger')
                return redirect(url_for('edit_inventory', inventory_id=inventory_id))

        return render_template("edit_inventory.html", inventory=inventory)

def delete_inventory(app):
    @app.route("/inventory/delete/<int:inventory_id>", methods=["POST"])
    def delete_inventory(inventory_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        inventory = Inventory.query.get_or_404(inventory_id)

        try:
            db.session.delete(inventory)
            db.session.commit()
            flash('Инвентарь успешно удален!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при удалении инвентаря. Попробуйте снова.', 'danger')

        return redirect(url_for('view_inventory'))
