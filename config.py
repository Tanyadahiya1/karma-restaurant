import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration for the Karma Indian Bistro & Restaurant website."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "karma-indian-bistro-jax-beach-super-secret-key-2026")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(basedir, "instance", "karma.db")
    )
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None

    RESTAURANT_NAME = "Karma Indian Bistro & Restaurant"
    RESTAURANT_TAGLINE = "Good Food. Good Mood. Good Karma."
    RESTAURANT_CITY = "Jacksonville Beach, Florida"
    RESTAURANT_PHONE = "(904) 372-4141"
    RESTAURANT_PHONE_RAW = "+19043724141"
    RESTAURANT_EMAIL = "info@karmabistrojax.com"
    RESTAURANT_ADDRESS = "1708 3rd St N, Jacksonville Beach, FL 32250"
    RESTAURANT_LAT = 30.3033
    RESTAURANT_LNG = -81.3976

    RESTAURANT_HOURS = [
        {"days": "Monday", "hours": "Closed"},
        {"days": "Tuesday - Thursday", "hours": "11:30 AM - 2:30 PM  |  5:00 PM - 9:15 PM"},
        {"days": "Friday - Saturday", "hours": "11:30 AM - 3:00 PM  |  5:00 PM - 9:30 PM"},
        {"days": "Sunday", "hours": "11:30 AM - 3:00 PM  |  5:00 PM - 9:15 PM"},
    ]

    SOCIAL_LINKS = {
        "facebook": "https://www.facebook.com/KarmaBistroJax/",
        "instagram": "https://www.instagram.com/karmabistrojax/",
    }

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    ADMIN_DEFAULT_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_DEFAULT_PASSWORD = os.environ.get("ADMIN_PASSWORD", "KarmaAdmin@2026")

    # ---- Stripe (set these in your environment / Render dashboard to go live) ----
    STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
    STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY", "")
    STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")

    # ---- Email (Flask-Mail — set these to enable real order/reservation emails) ----
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", "false").lower() == "true"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "Karma Indian Bistro <noreply@karmabistrojax.com>")
    OWNER_NOTIFICATION_EMAIL = os.environ.get("OWNER_NOTIFICATION_EMAIL", "info@karmabistrojax.com")


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True


class DevelopmentConfig(Config):
    DEBUG = True


config_map = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "default": DevelopmentConfig,
}
