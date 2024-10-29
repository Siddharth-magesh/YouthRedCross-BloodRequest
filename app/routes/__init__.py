# app/routes/__init__.py
from .main.main import main_bp
from .admin.admin import admin_bp
from .main.fetch_donors import fetch_availabe_donors
from .main.add_donor import new_donor
from .main.generate_blood_request import generate_blood_request
from .admin.admin_login import admin_authentications

def init_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(fetch_availabe_donors)
    app.register_blueprint(new_donor)
    app.register_blueprint(generate_blood_request)
    app.register_blueprint(admin_authentications)