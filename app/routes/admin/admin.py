# app/routes/admin.py
from flask import Blueprint, render_template
from app.utils.data_manipulations_toDB import FetchDetails

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/render_admin_login')
def render_admin_login():
    return render_template('admin_login.html')

@admin_bp.route('/render_main_admin_page')
def render_main_admin_page():
    return render_template('admin_main_page.html')

@admin_bp.route('/render_new_requests_page')
def render_new_requests_page():
    requests = FetchDetails.get_new_requests()
    return render_template('new_requests_admin.html',requests = requests)

@admin_bp.route('/render_request_approval_confirmation')
def render_request_approval_confirmation():
    print("Here")
    return render_template('request_approval_confirmation.html')

@admin_bp.route('/render_ongoing_requests_page')
def render_ongoing_requests_page():
    return render_template('ongoing_requests_admin.html')

@admin_bp.route('/render_analytics_page')
def render_analytics_page():
    return render_template('analytics_admin.html')

@admin_bp.route('/render_manage_donors_admin_page')
def render_manage_donors_admin_page():
    return render_template('manage_donors_admin.html')