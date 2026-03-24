"""
DUT Student Housing & Roommate Matching System - Application Factory
File: app/__init__.py
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
import os

# 1. Initialize extensions globally (Empty objects)
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()

# Login Management Security Settings
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app():
    """
    Application Factory: Creates and configures the Flask instance.
    """
    app = Flask(__name__)
    
    # 2. CORE SYSTEM CONFIGURATION
    app.config['SECRET_KEY'] = 'dev_key_2026_student_housing_portal'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 3. GMAIL EMAIL CONFIGURATION
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    
    # Credentials
    app.config['MAIL_USERNAME'] = 'asphilelubanyana@gmail.com'
    app.config['MAIL_PASSWORD'] = 'gzwlwgfnpoxqtmod' 
    app.config['MAIL_DEFAULT_SENDER'] = ('DUT Student Housing', 'asphilelubanyana@gmail.com')

    # 4. BINDING EXTENSIONS TO APP INSTANCE
    # This "attaches" the global objects to this specific app
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    # 5. BLUEPRINT REGISTRATION (Inside the factory to avoid Circular Imports)
    from app.routes.auth import auth as auth_blueprint
    from app.routes.main import main as main_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    # 6. DATABASE MODELS & USER SESSION LOADER
    with app.app_context():
        from app.models.user import User

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
            
        # Optional: Creates the database file if it doesn't exist
        # db.create_all() 

    return app

# Create app instance for production (Render/Gunicorn)
app = create_app()

# Initialize database on app startup
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Database Initialization Error: {e}")