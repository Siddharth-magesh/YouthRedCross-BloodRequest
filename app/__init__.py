from flask import Flask, current_app
from .config import Config
from .models import db
from .routes import init_blueprints
from datetime import timedelta
from flask_session import Session
from flask_session_captcha import FlaskSessionCaptcha
from flask_apscheduler import APScheduler
from app.utils.scheduled_automations import expire_blood_requests , increment_age , activate_donor_status
import os,time

scheduler = APScheduler()

def clean_expired_sessions():
    session_dir = os.path.join(os.getcwd(), 'flask_session')
    now = time.time()
    for filename in os.listdir(session_dir):
        file_path = os.path.join(session_dir, filename)
        if os.path.isfile(file_path):
            file_age = now - os.path.getmtime(file_path)
            if file_age > current_app.permanent_session_lifetime.total_seconds():
                os.remove(file_path)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.permanent_session_lifetime = timedelta(minutes=2)

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

    configure_scheduler(app)

    return app

def configure_scheduler(app):
    scheduler.init_app(app)

    @scheduler.task('cron', id='expire_requests_job', hour=0, minute=0)
    def expire_requests_job():
        with app.app_context():
            expire_blood_requests()

    @scheduler.task('cron',id='increment_age_job', hour=0, minute=0)
    def increment_age_job():
        with app.app_context():
            increment_age()

    @scheduler.task('cron',id='activate_donor_status_job', hour=0, minute=0)
    def activate_donor_status_job():
        with app.app_context():
            activate_donor_status()

    @scheduler.task('interval', id='clean_expired_sessions_job', minutes=5)
    def clean_expired_sessions_job():
        with app.app_context():
            clean_expired_sessions()

    scheduler.start()

