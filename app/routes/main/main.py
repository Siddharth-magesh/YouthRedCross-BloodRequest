# app/routes/main.py
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/render_find_donors_page')
def render_find_donors_page():
    return render_template('fetch_donors.html')

'''@main_bp.route('/admin-login')
def admin_login():
    return render_template('admin_login.html')'''

'''@main_bp.route('/generate-request')
def generate_request():
    return render_template('generate_request.html')

@main_bp.route('/about-us')
def about_us():
    return render_template('about_us.html')

@main_bp.route('/register-donor')
def register_donor():
    return render_template('register_donor.html')

@main_bp.route('/signing-user')
def signing_user():
    return render_template('signing_user.html')'''
