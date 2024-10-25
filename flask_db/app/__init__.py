from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Initialize extensions
from .connectors.db import db, init_db

login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    
    # Initialize database
    init_db(app)
    
    # Set secret key
    app.config['SECRET_KEY'] = 'your-secret-key'
    
    # Initialize extensions
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Import models untuk user_loader
    from .models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from .routes.auth import auth
    from .routes.main import main
    from .routes.review import review

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(review)

    return app