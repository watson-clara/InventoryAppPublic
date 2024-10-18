from flask import Flask
from config import Config
from app.extensions import db, login_manager  # Import db and login_manager from extensions
from app.user.routes import user as user_blueprint

def create_app():
    # Initialize the Flask application
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configuration from config.py

    # Initialize extensions
    db.init_app(app)               # Initialize SQLAlchemy
    login_manager.init_app(app)     # Initialize Flask-Login

    # Load the user_loader for Flask-Login
    from app.models.user import User  # Import User model

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints after app and extensions are initialized
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .inventory import inventory as inventory_blueprint
    app.register_blueprint(inventory_blueprint, url_prefix='/inventory')

    from .vendor import vendor as vendor_blueprint
    app.register_blueprint(vendor_blueprint, url_prefix='/vendor')

    app.register_blueprint(user_blueprint, url_prefix='/user')

    return app
