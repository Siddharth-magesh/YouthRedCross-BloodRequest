# app/routes/__init__.py
from .main import main_bp
from .admin import admin_bp
from .fetch_donors import fetch_availabe_donors

def init_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(fetch_availabe_donors)