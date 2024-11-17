from flask import render_template, redirect, url_for, flash, request, session
from models import *


def view_payments(app):
    @app.route("/view_payments", methods=["GET"])
    def view_payments():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        payments = Payment.query.all()
        return render_template("view_payments.html", payments=payments)


def add_payment(app):
    @app.route("/payments/add", methods=["GET", "POST"])
    def add_payment():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        if request.method == "POST":
            client_id = request.form['client_id']
            membership_id = request.form['membership_id']
            amount = request.form['amount']
            payment_date = request.form['payment_date']
            payment_method = request.form['payment_method']

            new_payment = Payment(
                client_id=client_id,
                membership_id=membership_id,
                amount=amount,
                payment_date=payment_date,
                payment_method=payment_method
            )

            try:
                db.session.add(new_payment)
                db.session.commit()
                flash('Платеж успешно добавлен!', 'success')
                return redirect(url_for('view_payments'))
            except Exception as e:
                db.session.rollback()
                flash('Ошибка при добавлении платежа. Попробуйте снова.', 'danger')
                return redirect(url_for('add_payment'))

        clients = Client.query.all()
        memberships = Membership.query.all()
        return render_template("add_payment.html", clients=clients, memberships=memberships)


def edit_payment(app):
    @app.route("/payments/edit/<int:payment_id>", methods=["GET", "POST"])
    def edit_payment(payment_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        payment = Payment.query.get_or_404(payment_id)

        if request.method == "POST":
            payment.client_id = request.form['client_id']
            payment.membership_id = request.form['membership_id']
            payment.amount = request.form['amount']
            payment.payment_date = request.form['payment_date']
            payment.payment_method = request.form['payment_method']

            try:
                db.session.commit()
                flash('Платеж успешно обновлен!', 'success')
                return redirect(url_for('view_payments'))
            except Exception as e:
                db.session.rollback()
                flash('Ошибка при обновлении платежа. Попробуйте снова.', 'danger')
                return redirect(url_for('edit_payment', payment_id=payment_id))

        clients = Client.query.all()
        memberships = Membership.query.all()
        return render_template("edit_payment.html", payment=payment, clients=clients, memberships=memberships)


def delete_payment(app):
    @app.route("/payments/delete/<int:payment_id>", methods=["POST"])
    def delete_payment(payment_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        payment = Payment.query.get_or_404(payment_id)

        try:
            db.session.delete(payment)
            db.session.commit()
            flash('Платеж успешно удален!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при удалении платежа. Попробуйте снова.', 'danger')

        return redirect(url_for('view_payments'))
