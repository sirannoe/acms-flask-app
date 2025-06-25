# app/__init__.py

from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from datetime import datetime
from config import Config
from dotenv import load_dotenv

from app.extensions import db, migrate, bcrypt
from app.utils.utils import generate_key_stats

load_dotenv()  # Load .env file locally

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # 🔐 Login manager setup
    login = LoginManager()
    login.init_app(app)
    login.login_view = "auth.login"
    login.login_message = "Please log in to access this page."

    from app.models import User

    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # 📌 Custom error page
    @app.errorhandler(403)
    def forbidden(e):
        return render_template("403.html"), 403

    # Context processors
    @app.context_processor
    def inject_now():
        return {"now": datetime.now}

    @app.context_processor
    def inject_key_stats():
        return {"key_stats": generate_key_stats()}

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.patients import patients_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.appointments import appointments_bp
    from app.routes.sms_test import sms_test_bp
    from app.routes.auth import auth_bp
    from app.routes.users import users_bp
    from app.routes.chatbot import chatbot_bp
    from app.routes.whatsapp import whatsapp_bp
    from app.routes.reports import reports_bp
    from app.routes.admin_portal import admin_bp
    from app.routes.reminders import reminders_bp
    from app.cli.seed import seed

    app.register_blueprint(main_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(sms_test_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(whatsapp_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(reminders_bp)

    # Custom CLI commands (e.g. flask seed)
    app.cli.add_command(seed)

    return app
