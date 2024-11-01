# app/routes/admin.py
from flask import Blueprint, render_template , request , redirect , url_for
from app.utils.data_manipulations_toDB import FetchDetails

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/render_admin_login')
def render_admin_login():
    return render_template('admin_login.html')

@admin_bp.route('/render_admin_signup')
def render_admin_signup():
    return render_template('admin_signup.html')

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
    requests = FetchDetails.fetch_ongoing_requests()
    return render_template('ongoing_requests_admin.html',requests = requests)

@admin_bp.route('/render_closed_requests_page')
def render_closed_requests_page():
    requests = FetchDetails.fetch_closed_requests()
    return render_template('closed_requests_admin.html',requests = requests)

@admin_bp.route('/render_expired_requests_page')
def render_expired_requests_page():
    requests = FetchDetails.fetch_expired_requests()
    return render_template('expired_requests_admin.html',requests = requests)

@admin_bp.route('/render_analytics_page')
def render_analytics_page():
    data = FetchDetails.generate_analytics()
    return render_template(
        'analytics_admin.html',
        hospital_count=data['hospital_count'],
        recent_donor_count=data['recent_donor_count'],
        recent_request_count=data['recent_request_count']
    )

@admin_bp.route('/render_manage_donors_admin_page')
def render_manage_donors_admin_page():
    donors = FetchDetails.fetch_all_donors()
    return render_template('manage_donors_admin.html',donors=donors)

@admin_bp.route('/render_donor_modification_page',methods=['POST','GET'])
def render_donor_modification_page():
    donor_id = request.form.get('donor_id')
    details = FetchDetails.fetch_donor_details(donor_id)
    return render_template('manage_each_donor_admin.html',details=details)