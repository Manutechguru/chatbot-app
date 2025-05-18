from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # or change if login view is elsewhere

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # Import models so SQLAlchemy knows them
    from .models import User
    from . import routes, services

    # ✅ Register user_loader BEFORE app context
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from .auth import bp as auth_bp
    from .routes import routes as routes_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(routes_bp)

    # Create tables inside app context
    with app.app_context():
        db.create_all()

    return app
