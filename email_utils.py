from flask import current_app, render_template
from flask_mail import Message

from extensions import mail


def _mail_configured():
    return bool(current_app.config.get("MAIL_SERVER") and current_app.config.get("MAIL_USERNAME"))


def _send(subject, recipients, html_body):
    """Send an email if mail is configured; otherwise log and skip silently.

    This ensures checkout/reservation flows never break just because SMTP
    credentials haven't been added to the environment yet.
    """
    if not _mail_configured():
        current_app.logger.info(
            "MAIL not configured — skipping email '%s' to %s. "
            "Set MAIL_SERVER / MAIL_USERNAME / MAIL_PASSWORD to enable real emails.",
            subject, recipients,
        )
        return False
    try:
        msg = Message(subject=subject, recipients=recipients, html=html_body)
        mail.send(msg)
        return True
    except Exception as exc:  # noqa: BLE001 - never let email failures break the request
        current_app.logger.warning("Failed to send email '%s' to %s: %s", subject, recipients, exc)
        return False


def send_order_customer_email(order):
    restaurant_name = current_app.config["RESTAURANT_NAME"]
    subject = f"Your {restaurant_name} Order #{order.order_number} is Confirmed"
    html = render_template("emails/order_customer.html", order=order)
    return _send(subject, [order.email], html)


def send_order_owner_email(order):
    owner_email = current_app.config["OWNER_NOTIFICATION_EMAIL"]
    subject = f"🔔 New Order #{order.order_number} — ${order.total:.2f} ({order.order_type.title()})"
    html = render_template("emails/order_owner.html", order=order)
    return _send(subject, [owner_email], html)


def send_reservation_customer_email(reservation):
    restaurant_name = current_app.config["RESTAURANT_NAME"]
    subject = f"Your Reservation at {restaurant_name} — Confirmation #{reservation.id:05d}"
    html = render_template("emails/reservation_customer.html", reservation=reservation)
    return _send(subject, [reservation.email], html)


def send_reservation_owner_email(reservation):
    owner_email = current_app.config["OWNER_NOTIFICATION_EMAIL"]
    subject = f"📅 New Reservation Request — {reservation.name} ({reservation.guests} guests, {reservation.date})"
    html = render_template("emails/reservation_owner.html", reservation=reservation)
    return _send(subject, [owner_email], html)
