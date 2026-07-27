import csv
import io

from flask import (
    Blueprint, render_template, redirect, url_for, flash, request, Response
)
from flask_login import login_user, logout_user, login_required, current_user

from models import db, AdminUser, Order, Reservation, ContactMessage, NewsletterSubscriber, MenuItem
from forms import LoginForm

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = AdminUser.query.filter_by(username=form.username.data.strip()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f"Welcome back, {user.username}!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("admin.dashboard"))
        flash("Invalid username or password.", "danger")
    return render_template("login.html", form=form)


@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("admin.login"))


@admin_bp.route("/")
@login_required
def dashboard():
    stats = {
        "orders_count": Order.query.count(),
        "reservations_count": Reservation.query.count(),
        "messages_count": ContactMessage.query.count(),
        "unread_messages": ContactMessage.query.filter_by(is_read=False).count(),
        "newsletter_count": NewsletterSubscriber.query.count(),
        "pending_reservations": Reservation.query.filter_by(status="Pending").count(),
        "revenue": round(sum(o.total for o in Order.query.all()), 2),
        "menu_items_count": MenuItem.query.count(),
    }
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    recent_reservations = Reservation.query.order_by(Reservation.created_at.desc()).limit(5).all()
    return render_template("admin.html", view="dashboard", stats=stats,
                            recent_orders=recent_orders, recent_reservations=recent_reservations)


@admin_bp.route("/orders")
@login_required
def orders():
    search = request.args.get("q", "").strip()
    query = Order.query
    if search:
        query = query.filter(
            (Order.order_number.ilike(f"%{search}%")) |
            (Order.customer_name.ilike(f"%{search}%")) |
            (Order.phone.ilike(f"%{search}%"))
        )
    all_orders = query.order_by(Order.created_at.desc()).all()
    return render_template("admin.html", view="orders", orders=all_orders, search_query=search)


@admin_bp.route("/orders/<int:order_id>/status", methods=["POST"])
@login_required
def update_order_status(order_id):
    order_obj = Order.query.get_or_404(order_id)
    order_obj.status = request.form.get("status", order_obj.status)
    db.session.commit()
    flash(f"Order {order_obj.order_number} updated to {order_obj.status}.", "success")
    return redirect(url_for("admin.orders"))


@admin_bp.route("/orders/<int:order_id>/delete", methods=["POST"])
@login_required
def delete_order(order_id):
    order_obj = Order.query.get_or_404(order_id)
    db.session.delete(order_obj)
    db.session.commit()
    flash("Order deleted.", "info")
    return redirect(url_for("admin.orders"))


@admin_bp.route("/orders/export")
@login_required
def export_orders():
    return _export_csv(
        Order.query.order_by(Order.created_at.desc()).all(),
        ["order_number", "customer_name", "phone", "email", "order_type", "items_json",
         "subtotal", "discount", "tax", "total", "payment_method", "status", "created_at"],
        "orders.csv",
    )


@admin_bp.route("/reservations")
@login_required
def reservations():
    search = request.args.get("q", "").strip()
    query = Reservation.query
    if search:
        query = query.filter(
            (Reservation.name.ilike(f"%{search}%")) | (Reservation.phone.ilike(f"%{search}%"))
        )
    all_reservations = query.order_by(Reservation.created_at.desc()).all()
    return render_template("admin.html", view="reservations", reservations=all_reservations, search_query=search)


@admin_bp.route("/reservations/<int:res_id>/status", methods=["POST"])
@login_required
def update_reservation_status(res_id):
    res_obj = Reservation.query.get_or_404(res_id)
    res_obj.status = request.form.get("status", res_obj.status)
    db.session.commit()
    flash(f"Reservation for {res_obj.name} updated to {res_obj.status}.", "success")
    return redirect(url_for("admin.reservations"))


@admin_bp.route("/reservations/<int:res_id>/delete", methods=["POST"])
@login_required
def delete_reservation(res_id):
    res_obj = Reservation.query.get_or_404(res_id)
    db.session.delete(res_obj)
    db.session.commit()
    flash("Reservation deleted.", "info")
    return redirect(url_for("admin.reservations"))


@admin_bp.route("/reservations/export")
@login_required
def export_reservations():
    return _export_csv(
        Reservation.query.order_by(Reservation.created_at.desc()).all(),
        ["name", "phone", "email", "guests", "date", "time", "special_requests", "status", "created_at"],
        "reservations.csv",
    )


@admin_bp.route("/messages")
@login_required
def messages():
    all_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template("admin.html", view="messages", messages=all_messages)


@admin_bp.route("/messages/<int:msg_id>/read", methods=["POST"])
@login_required
def mark_message_read(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    msg.is_read = True
    db.session.commit()
    return redirect(url_for("admin.messages"))


@admin_bp.route("/messages/<int:msg_id>/delete", methods=["POST"])
@login_required
def delete_message(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    db.session.delete(msg)
    db.session.commit()
    flash("Message deleted.", "info")
    return redirect(url_for("admin.messages"))


@admin_bp.route("/newsletter")
@login_required
def newsletter():
    subscribers = NewsletterSubscriber.query.order_by(NewsletterSubscriber.created_at.desc()).all()
    return render_template("admin.html", view="newsletter", subscribers=subscribers)


@admin_bp.route("/newsletter/<int:sub_id>/delete", methods=["POST"])
@login_required
def delete_subscriber(sub_id):
    sub = NewsletterSubscriber.query.get_or_404(sub_id)
    db.session.delete(sub)
    db.session.commit()
    flash("Subscriber removed.", "info")
    return redirect(url_for("admin.newsletter"))


@admin_bp.route("/newsletter/export")
@login_required
def export_newsletter():
    return _export_csv(
        NewsletterSubscriber.query.order_by(NewsletterSubscriber.created_at.desc()).all(),
        ["email", "created_at"],
        "newsletter_subscribers.csv",
    )


@admin_bp.route("/menu")
@login_required
def menu_management():
    items = MenuItem.query.order_by(MenuItem.category, MenuItem.name).all()
    return render_template("admin.html", view="menu", menu_items=items)


@admin_bp.route("/menu/<int:item_id>/toggle", methods=["POST"])
@login_required
def toggle_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    item.is_available = not item.is_available
    db.session.commit()
    flash(f"{item.name} is now {'available' if item.is_available else 'hidden'}.", "success")
    return redirect(url_for("admin.menu_management"))


def _export_csv(records, fields, filename):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(fields)
    for record in records:
        writer.writerow([getattr(record, f) for f in fields])
    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response
