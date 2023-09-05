"""
Flask Web Application

This is the main module for the Flask web application.
It serves as the entry point for the application package.
The application is designed to be a simple task management system.

Directory Structure:
    - `templates`: Stores HTML templates for rendering views.
    - `static`: Stores static files (CSS, JavaScript, etc.).


Modules:
    - `routes`: Contains route definitions for creating, listing, and managing tasks.
    - `models`: Defines the Task model for the database.
    - `config`: Configuration settings for the application.
"""


from flask import Flask, current_app
from flask_login import LoginManager
from flasgger import Swagger
from app.models import db, User

def create_app():
    """
    This function will initialize the flask application and create a Login manager.
    This will also register a API blueprint

    """
    app = Flask(__name__)
    swagger = Swagger(app)
    app.config.from_pyfile('../config.py')
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Initialize Flask-Login
    global login_manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from app.routes import api_bp
    # Register the API blueprint
    app.register_blueprint(api_bp, url_prefix='/')

    return app
