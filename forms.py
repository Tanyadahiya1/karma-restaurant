from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    IntegerField,
    PasswordField,
)
from wtforms.validators import DataRequired, Email, Length, NumberRange, Regexp, Optional, EqualTo


class ReservationForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=120)])
    phone = StringField(
        "Phone Number",
        validators=[DataRequired(), Regexp(r"^[0-9+\-\s()]{7,20}$", message="Enter a valid phone number")],
    )
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    guests = IntegerField("Number of Guests", validators=[DataRequired(), NumberRange(min=1, max=30)])
    date = StringField("Date", validators=[DataRequired()])
    time = StringField("Time", validators=[DataRequired()])
    special_requests = TextAreaField("Special Requests", validators=[Length(max=500)])


class ContactForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField("Phone", validators=[Length(max=30)])
    subject = StringField("Subject", validators=[Length(max=200)])
    message = TextAreaField("Message", validators=[DataRequired(), Length(min=10, max=2000)])


class NewsletterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])


class CheckoutForm(FlaskForm):
    customer_name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=120)])
    phone = StringField(
        "Phone Number",
        validators=[DataRequired(), Regexp(r"^[0-9+\-\s()]{7,20}$", message="Enter a valid phone number")],
    )
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    order_type = SelectField(
        "Order Type", choices=[("pickup", "Pickup"), ("delivery", "Delivery")], validators=[DataRequired()]
    )
    address = TextAreaField("Delivery Address", validators=[Length(max=300)])
    payment_method = SelectField(
        "Payment Method",
        choices=[
            ("Pay Online (Card via Stripe)", "Pay Online — Secure Card Checkout"),
            ("Pay at Counter", "Pay at Counter"),
            ("Cash on Delivery", "Cash on Delivery"),
        ],
        validators=[DataRequired()],
    )
    coupon_code = StringField("Coupon Code", validators=[Length(max=40)])
    notes = TextAreaField("Order Notes", validators=[Length(max=400)])


class RegisterForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField(
        "Phone Number",
        validators=[DataRequired(), Regexp(r"^[0-9+\-\s()]{7,20}$", message="Enter a valid phone number")],
    )
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, message="Use at least 8 characters")])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match")]
    )


class CustomerLoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=80)])
    password = PasswordField("Password", validators=[DataRequired()])
