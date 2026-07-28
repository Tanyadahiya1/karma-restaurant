import random
import string

import stripe
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session, current_app

from extensions import csrf
from models import db, MenuItem, Order
from forms import CheckoutForm
from email_utils import send_order_customer_email, send_order_owner_email
from routes.auth import get_current_customer

order_bp = Blueprint("order", __name__)

COUPONS = {
    "KARMA10": 0.10,
    "WELCOME15": 0.15,
    "JAXBEACH20": 0.20,
}
TAX_RATE = 0.075


def _get_cart():
    return session.setdefault("cart", {})


def _cart_items_detail(cart):
    items = []
    subtotal = 0.0
    if not cart:
        return items, subtotal
    ids = [int(i) for i in cart.keys()]
    menu_items = {m.id: m for m in MenuItem.query.filter(MenuItem.id.in_(ids)).all()}
    for item_id, qty in cart.items():
        menu_item = menu_items.get(int(item_id))
        if not menu_item:
            continue
        line_total = menu_item.price * qty
        subtotal += line_total
        items.append({"item": menu_item, "qty": qty, "line_total": line_total})
    return items, subtotal


@order_bp.route("/order")
def order_online():
    items = MenuItem.query.filter_by(is_available=True).order_by(MenuItem.category, MenuItem.name).all()
    return render_template("order.html", items=items)


@order_bp.route("/cart/add", methods=["POST"])
def cart_add():
    data = request.get_json(silent=True) or request.form
    item_id = str(data.get("item_id"))
    qty = int(data.get("qty", 1))

    menu_item = MenuItem.query.get(item_id)
    if not menu_item or not menu_item.is_available:
        return jsonify({"ok": False, "message": "Item not available."}), 404

    cart = _get_cart()
    cart[item_id] = cart.get(item_id, 0) + max(1, qty)
    session["cart"] = cart
    session.modified = True

    count = sum(cart.values())
    return jsonify({"ok": True, "message": f"{menu_item.name} added to cart.", "cart_count": count})


@order_bp.route("/cart/update", methods=["POST"])
def cart_update():
    data = request.get_json(silent=True) or request.form
    item_id = str(data.get("item_id"))
    qty = int(data.get("qty", 1))

    cart = _get_cart()
    if item_id in cart:
        if qty <= 0:
            cart.pop(item_id)
        else:
            cart[item_id] = qty
        session["cart"] = cart
        session.modified = True

    items, subtotal = _cart_items_detail(cart)
    return jsonify({
        "ok": True,
        "cart_count": sum(cart.values()),
        "subtotal": round(subtotal, 2),
    })


@order_bp.route("/cart/remove", methods=["POST"])
def cart_remove():
    data = request.get_json(silent=True) or request.form
    item_id = str(data.get("item_id"))
    cart = _get_cart()
    cart.pop(item_id, None)
    session["cart"] = cart
    session.modified = True
    items, subtotal = _cart_items_detail(cart)
    return jsonify({"ok": True, "cart_count": sum(cart.values()), "subtotal": round(subtotal, 2)})


@order_bp.route("/cart")
def cart_view():
    cart = _get_cart()
    items, subtotal = _cart_items_detail(cart)
    return render_template("order.html", cart_items=items, subtotal=subtotal, show_cart=True,
                            items=MenuItem.query.filter_by(is_available=True).order_by(MenuItem.category).all())


@order_bp.route("/cart/apply-coupon", methods=["POST"])
def apply_coupon():
    data = request.get_json(silent=True) or request.form
    code = (data.get("coupon_code") or "").strip().upper()
    cart = _get_cart()
    items, subtotal = _cart_items_detail(cart)

    if code not in COUPONS:
        return jsonify({"ok": False, "message": "Invalid or expired coupon code."}), 400

    discount = round(subtotal * COUPONS[code], 2)
    tax = round((subtotal - discount) * TAX_RATE, 2)
    total = round(subtotal - discount + tax, 2)
    return jsonify({
        "ok": True,
        "message": f"Coupon applied: {int(COUPONS[code] * 100)}% off",
        "discount": discount,
        "tax": tax,
        "total": total,
    })


def _build_order(form, items, subtotal, customer):
    coupon_code = (form.coupon_code.data or "").strip().upper()
    discount_rate = COUPONS.get(coupon_code, 0.0)
    discount = round(subtotal * discount_rate, 2)
    tax = round((subtotal - discount) * TAX_RATE, 2)
    total = round(subtotal - discount + tax, 2)

    order_number = "KI" + "".join(random.choices(string.digits, k=6))
    items_json = ", ".join(f"{d['item'].name} x{d['qty']}" for d in items)

    order = Order(
        order_number=order_number,
        customer_id=customer.id if customer else None,
        customer_name=form.customer_name.data.strip(),
        phone=form.phone.data.strip(),
        email=form.email.data.strip(),
        order_type=form.order_type.data,
        address=form.address.data.strip() if form.order_type.data == "delivery" else None,
        items_json=items_json,
        subtotal=round(subtotal, 2),
        discount=discount,
        coupon_code=coupon_code if discount_rate else None,
        tax=tax,
        total=total,
        payment_method=form.payment_method.data,
        payment_status="Unpaid",
        notes=form.notes.data.strip() if form.notes.data else None,
    )
    db.session.add(order)
    db.session.commit()
    return order


def _finalize_paid_order(order):
    """Mark an order paid and fire the confirmation / owner emails exactly once."""
    if order.payment_status == "Paid":
        return  # already finalized (e.g. webhook fired after success-page redirect)
    order.payment_status = "Paid"
    order.status = "Confirmed"
    db.session.commit()
    send_order_customer_email(order)
    send_order_owner_email(order)


@order_bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart = _get_cart()
    items, subtotal = _cart_items_detail(cart)

    if not items:
        flash("Your cart is empty. Add some delicious items from the menu first!", "warning")
        return redirect(url_for("order.order_online"))

    customer = get_current_customer()
    form = CheckoutForm()
    if request.method == "GET" and customer:
        form.customer_name.data = customer.name
        form.email.data = customer.email
        form.phone.data = customer.phone

    if form.validate_on_submit():
        order = _build_order(form, items, subtotal, customer)

        if form.payment_method.data == "Pay Online (Card via Stripe)":
            if not current_app.config.get("STRIPE_SECRET_KEY"):
                flash(
                    "Online card payment isn't configured yet on this server. "
                    "Please choose 'Pay at Counter' or 'Cash on Delivery' for now.",
                    "warning",
                )
                db.session.delete(order)
                db.session.commit()
                return redirect(url_for("order.checkout"))

            stripe.api_key = current_app.config["STRIPE_SECRET_KEY"]
            try:
                checkout_session = stripe.checkout.Session.create(
                    mode="payment",
                    payment_method_types=["card"],
                    customer_email=order.email,
                    line_items=[{
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": f"Karma Indian Bistro — Order #{order.order_number}",
                                "description": order.items_json[:250],
                            },
                            "unit_amount": int(round(order.total * 100)),
                        },
                        "quantity": 1,
                    }],
                    metadata={"order_number": order.order_number},
                    success_url=url_for("order.stripe_success", _external=True) + "?session_id={CHECKOUT_SESSION_ID}",
                    cancel_url=url_for("order.stripe_cancel", order_number=order.order_number, _external=True),
                )
            except Exception as exc:  # noqa: BLE001
                current_app.logger.warning("Stripe session creation failed: %s", exc)
                flash("We couldn't start the secure card checkout. Please try again or choose another payment method.", "danger")
                db.session.delete(order)
                db.session.commit()
                return redirect(url_for("order.checkout"))

            order.stripe_session_id = checkout_session.id
            db.session.commit()
            return redirect(checkout_session.url, code=303)

        # Pay at Counter / Cash on Delivery — order is placed immediately.
        session["cart"] = {}
        session.modified = True
        send_order_customer_email(order)
        send_order_owner_email(order)
        return redirect(url_for("order.order_confirmation", order_number=order.order_number))

    tax = round(subtotal * TAX_RATE, 2)
    total = round(subtotal + tax, 2)
    return render_template("order.html", form=form, cart_items=items, subtotal=subtotal,
                            tax=tax, total=total, show_checkout=True, items=[],
                            stripe_publishable_key=current_app.config.get("STRIPE_PUBLISHABLE_KEY"))


@order_bp.route("/order/stripe/success")
def stripe_success():
    session_id = request.args.get("session_id")
    if not session_id:
        flash("Missing payment session.", "danger")
        return redirect(url_for("order.order_online"))

    stripe.api_key = current_app.config["STRIPE_SECRET_KEY"]
    try:
        checkout_session = stripe.checkout.Session.retrieve(session_id)
    except Exception as exc:  # noqa: BLE001
        current_app.logger.warning("Stripe session retrieve failed: %s", exc)
        flash("We couldn't verify your payment. Please contact us with your order number.", "danger")
        return redirect(url_for("order.order_online"))

    order_number = (checkout_session.metadata or {}).get("order_number")
    order = Order.query.filter_by(order_number=order_number).first_or_404()

    if checkout_session.payment_status == "paid":
        order.stripe_payment_intent = checkout_session.payment_intent
        _finalize_paid_order(order)
        session["cart"] = {}
        session.modified = True
    else:
        flash("Payment was not completed. Please try again.", "warning")
        return redirect(url_for("order.checkout"))

    return redirect(url_for("order.order_confirmation", order_number=order.order_number))


@order_bp.route("/order/stripe/cancel/<order_number>")
def stripe_cancel(order_number):
    order = Order.query.filter_by(order_number=order_number).first()
    if order and order.payment_status != "Paid":
        db.session.delete(order)
        db.session.commit()
    flash("Checkout was cancelled — your cart has been kept so you can try again.", "info")
    return redirect(url_for("order.cart_view"))


@order_bp.route("/webhook/stripe", methods=["POST"])
@csrf.exempt
def stripe_webhook():
    webhook_secret = current_app.config.get("STRIPE_WEBHOOK_SECRET")
    if not webhook_secret:
        # Without a signing secret we cannot verify the payload is really from Stripe,
        # so we refuse to process it rather than trusting an unauthenticated request.
        current_app.logger.warning("Stripe webhook called but STRIPE_WEBHOOK_SECRET is not configured.")
        return jsonify({"error": "webhook not configured"}), 400

    payload = request.data
    sig_header = request.headers.get("Stripe-Signature", "")
    stripe.api_key = current_app.config.get("STRIPE_SECRET_KEY")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except Exception as exc:  # noqa: BLE001
        current_app.logger.warning("Stripe webhook verification failed: %s", exc)
        return jsonify({"error": "invalid signature"}), 400

    if event["type"] == "checkout.session.completed":
        data = event["data"]["object"]
        order_number = (data.get("metadata") or {}).get("order_number")
        order = Order.query.filter_by(order_number=order_number).first()
        if order and data.get("payment_status") == "paid":
            order.stripe_payment_intent = data.get("payment_intent")
            _finalize_paid_order(order)

    return jsonify({"received": True})


@order_bp.route("/order/confirmation/<order_number>")
def order_confirmation(order_number):
    order_obj = Order.query.filter_by(order_number=order_number).first_or_404()
    return render_template("order_confirmation.html", order=order_obj)
