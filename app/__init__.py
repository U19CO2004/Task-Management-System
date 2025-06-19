from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # Import blueprints
    from app.auth.routes import auth_bp
    from app.user_management.routes import user_management_bp
    from app.tasks.routes import tasks_bp

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_management_bp)
    app.register_blueprint(tasks_bp)
    
    return app
