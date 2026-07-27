from flask import Blueprint, render_template, redirect, url_for, flash, request, session

from models import db, Customer, Order, Reservation
from forms import RegisterForm, CustomerLoginForm

auth_bp = Blueprint("auth", __name__, url_prefix="/account")


def get_current_customer():
    """Return the logged-in Customer for this session, or None."""
    customer_id = session.get("customer_id")
    if not customer_id:
        return None
    return db.session.get(Customer, customer_id)


def login_customer(customer):
    session["customer_id"] = customer.id
    session.permanent = True


def logout_customer():
    session.pop("customer_id", None)


def customer_login_required(view_func):
    from functools import wraps

    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not get_current_customer():
            flash("Please sign in to view your account.", "warning")
            return redirect(url_for("auth.login", next=request.path))
        return view_func(*args, **kwargs)

    return wrapped


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if get_current_customer():
        return redirect(url_for("auth.dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        existing = Customer.query.filter_by(email=form.email.data.strip().lower()).first()
        if existing:
            flash("An account with that email already exists. Please sign in instead.", "warning")
            return redirect(url_for("auth.login"))

        customer = Customer(
            name=form.name.data.strip(),
            email=form.email.data.strip().lower(),
            phone=form.phone.data.strip(),
        )
        customer.set_password(form.password.data)
        db.session.add(customer)
        db.session.commit()

        login_customer(customer)
        flash(f"Welcome to Karma, {customer.name}! Your account has been created.", "success")
        return redirect(url_for("auth.dashboard"))

    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if get_current_customer():
        return redirect(url_for("auth.dashboard"))

    form = CustomerLoginForm()
    if form.validate_on_submit():
        customer = Customer.query.filter_by(email=form.email.data.strip().lower()).first()
        if customer and customer.check_password(form.password.data):
            login_customer(customer)
            flash(f"Welcome back, {customer.name}!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("auth.dashboard"))
        flash("Incorrect email or password.", "danger")

    return render_template("account_login.html", form=form)


@auth_bp.route("/logout")
def logout():
    logout_customer()
    flash("You have been signed out.", "info")
    return redirect(url_for("main.index"))


@auth_bp.route("/")
@customer_login_required
def dashboard():
    customer = get_current_customer()
    orders = Order.query.filter(
        (Order.customer_id == customer.id) | (Order.email == customer.email)
    ).order_by(Order.created_at.desc()).all()
    reservations = Reservation.query.filter(
        (Reservation.customer_id == customer.id) | (Reservation.email == customer.email)
    ).order_by(Reservation.created_at.desc()).all()
    return render_template("account.html", customer=customer, orders=orders, reservations=reservations)
