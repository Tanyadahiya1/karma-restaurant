import os
from datetime import datetime

from flask import Flask, render_template, session

from config import config_map
from extensions import login_manager, csrf, mail
from models import db, AdminUser, MenuItem
from seed import get_menu_items_with_slugs


def create_app(config_name=None):
    app = Flask(__name__, instance_relative_config=True)

    config_name = config_name or os.environ.get("FLASK_ENV", "default")
    app.config.from_object(config_map.get(config_name, config_map["default"]))

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)

    from routes.main import main_bp
    from routes.order import order_bp
    from routes.admin import admin_bp
    from routes.auth import auth_bp, get_current_customer

    app.register_blueprint(main_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(auth_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(AdminUser, int(user_id))

    @app.context_processor
    def inject_globals():
        customer = get_current_customer()
        return {
            "restaurant_name": app.config["RESTAURANT_NAME"],
            "restaurant_tagline": app.config["RESTAURANT_TAGLINE"],
            "restaurant_city": app.config["RESTAURANT_CITY"],
            "restaurant_phone": app.config["RESTAURANT_PHONE"],
            "restaurant_phone_raw": app.config["RESTAURANT_PHONE_RAW"],
            "restaurant_email": app.config["RESTAURANT_EMAIL"],
            "restaurant_address": app.config["RESTAURANT_ADDRESS"],
            "restaurant_hours": app.config["RESTAURANT_HOURS"],
            "restaurant_lat": app.config["RESTAURANT_LAT"],
            "restaurant_lng": app.config["RESTAURANT_LNG"],
            "social_links": app.config["SOCIAL_LINKS"],
            "current_year": datetime.utcnow().year,
            "cart_count": sum(session.get("cart", {}).values()) if session.get("cart") else 0,
            "customer": customer,
        }

    @app.teardown_request
    def cleanup_db_session(exception=None):
        if exception is not None:
            db.session.rollback()

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        db.session.rollback()
        try:
            return render_template("500.html"), 500
        except Exception:
            return "Something went wrong on our end. Please try again shortly.", 500

    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

    with app.app_context():
        db.create_all()
        _seed_database(app)

    return app


def _seed_database(app):
    """Populate the database with the initial menu catalog and a default admin user."""
    if MenuItem.query.first() is None:
        try:
            for item in get_menu_items_with_slugs():
                db.session.add(MenuItem(**item))
            db.session.commit()
            app.logger.info("Seeded menu items.")
        except Exception as exc:
            db.session.rollback()
            app.logger.warning("Menu seed skipped (likely already seeded by another worker): %s", exc)

    if AdminUser.query.first() is None:
        try:
            admin = AdminUser(
                username=app.config["ADMIN_DEFAULT_USERNAME"],
                email=app.config["RESTAURANT_EMAIL"],
            )
            admin.set_password(app.config["ADMIN_DEFAULT_PASSWORD"])
            db.session.add(admin)
            db.session.commit()
            app.logger.info("Created default admin user.")
        except Exception as exc:
            db.session.rollback()
            app.logger.warning("Admin seed skipped (likely already seeded by another worker): %s", exc)


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=app.config.get("DEBUG", False))
