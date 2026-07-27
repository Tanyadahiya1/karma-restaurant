from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app, Response

from extensions import csrf
from models import db, MenuItem, Reservation, ContactMessage, NewsletterSubscriber
from forms import ReservationForm, ContactForm, NewsletterForm
from email_utils import send_reservation_customer_email, send_reservation_owner_email
from routes.auth import get_current_customer

main_bp = Blueprint("main", __name__)

MENU_CATEGORIES = [
    "Appetizers",
    "Vegetarian",
    "Non Vegetarian",
    "Biryani",
    "South Indian",
    "Tandoor",
    "Bread",
    "Desserts",
    "Drinks",
]


@main_bp.route("/")
def index():
    popular_items = MenuItem.query.filter_by(is_popular=True, is_available=True).limit(8).all()
    return render_template("index.html", popular_items=popular_items)


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/menu")
def menu():
    category = request.args.get("category", "All")
    search = request.args.get("q", "").strip()

    query = MenuItem.query.filter_by(is_available=True)
    if category != "All" and category in MENU_CATEGORIES:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(MenuItem.name.ilike(f"%{search}%"))

    items = query.order_by(MenuItem.category, MenuItem.name).all()

    grouped = {}
    for item in items:
        grouped.setdefault(item.category, []).append(item)

    return render_template(
        "menu.html",
        grouped_items=grouped,
        categories=MENU_CATEGORIES,
        active_category=category,
        search_query=search,
    )


@main_bp.route("/gallery")
def gallery():
    return render_template("gallery.html")


@main_bp.route("/reservation", methods=["GET", "POST"])
def reservation():
    form = ReservationForm()
    customer = get_current_customer()
    if request.method == "GET" and customer:
        form.name.data = customer.name
        form.email.data = customer.email
        form.phone.data = customer.phone

    if form.validate_on_submit():
        reservation_obj = Reservation(
            customer_id=customer.id if customer else None,
            name=form.name.data.strip(),
            phone=form.phone.data.strip(),
            email=form.email.data.strip(),
            guests=form.guests.data,
            date=form.date.data,
            time=form.time.data,
            special_requests=form.special_requests.data.strip() if form.special_requests.data else None,
        )
        db.session.add(reservation_obj)
        db.session.commit()

        send_reservation_customer_email(reservation_obj)
        send_reservation_owner_email(reservation_obj)

        flash(
            f"Thank you, {reservation_obj.name}! Your table for {reservation_obj.guests} on "
            f"{reservation_obj.date} at {reservation_obj.time} has been requested. "
            f"A confirmation has been sent to {reservation_obj.email}.",
            "success",
        )
        return redirect(url_for("main.reservation"))
    return render_template("reservation.html", form=form, today=datetime.utcnow().strftime("%Y-%m-%d"))


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        message = ContactMessage(
            name=form.name.data.strip(),
            email=form.email.data.strip(),
            phone=form.phone.data.strip() if form.phone.data else None,
            subject=form.subject.data.strip() if form.subject.data else "General Enquiry",
            message=form.message.data.strip(),
        )
        db.session.add(message)
        db.session.commit()
        flash("Your message has been sent. Our team will get back to you within 24 hours.", "success")
        return redirect(url_for("main.contact"))
    return render_template("contact.html", form=form)


@main_bp.route("/newsletter/subscribe", methods=["POST"])
def newsletter_subscribe():
    form = NewsletterForm()
    if form.validate_on_submit():
        existing = NewsletterSubscriber.query.filter_by(email=form.email.data.strip().lower()).first()
        if existing:
            return jsonify({"ok": True, "message": "You're already on our list. Thank you!"})
        db.session.add(NewsletterSubscriber(email=form.email.data.strip().lower()))
        db.session.commit()
        return jsonify({"ok": True, "message": "Subscribed! Watch your inbox for Karma specials."})
    return jsonify({"ok": False, "message": "Please enter a valid email address."}), 400


@main_bp.route("/robots.txt")
def robots_txt():
    lines = [
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {request.url_root}sitemap.xml",
    ]
    return Response("\n".join(lines), mimetype="text/plain")


@main_bp.route("/sitemap.xml")
def sitemap_xml():
    pages = [
        url_for("main.index", _external=True),
        url_for("main.about", _external=True),
        url_for("main.menu", _external=True),
        url_for("main.gallery", _external=True),
        url_for("main.reservation", _external=True),
        url_for("order.order_online", _external=True),
        url_for("main.contact", _external=True),
    ]
    xml_items = "".join(f"<url><loc>{p}</loc></url>" for p in pages)
    xml = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{xml_items}</urlset>'
    return Response(xml, mimetype="application/xml")
