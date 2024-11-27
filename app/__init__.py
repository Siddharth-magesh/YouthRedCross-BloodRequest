from flask import Flask
from .config import Config
from .models import db
from .routes import init_blueprints
from datetime import timedelta
from flask_session import Session
from flask_session_captcha import FlaskSessionCaptcha

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.permanent_session_lifetime = timedelta(days=1)

    # Initialize database
    db.init_app(app)

    # Initialize session and captcha
    Session(app=app)
    captcha = FlaskSessionCaptcha(app)
    app.extensions['captcha'] = captcha

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Initialize blueprints
    init_blueprints(app)
    return app
