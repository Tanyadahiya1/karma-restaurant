from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_mail import Mail

login_manager = LoginManager()
login_manager.login_view = "admin.login"
login_manager.login_message = "Please log in to access the admin panel."
login_manager.login_message_category = "warning"

csrf = CSRFProtect()
mail = Mail()
