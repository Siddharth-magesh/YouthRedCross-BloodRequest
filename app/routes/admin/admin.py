# app/routes/admin.py
import os
from flask import Blueprint, render_template ,request
from flask_wtf import FlaskForm
from wtforms import SubmitField ,FileField
from wtforms.validators import InputRequired
from app.utils.data_manipulations_toDB import FetchDetails
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import pandas as pd

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

class AddDonorCSV(FlaskForm):
    donor_file = FileField('Donor CSV File', validators=[InputRequired()])
    submit = SubmitField('Upload')

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
    return render_template('analytics_admin.html')

@admin_bp.route('/render_manage_donors_admin_page')
def render_manage_donors_admin_page():
    return render_template('manage_donors_admin.html')

@admin_bp.route('/add_donor_csv', methods=['POST','GET'])
def add_donor_csv():
    form = AddDonorCSV()
    if request.method == 'POST' and form.validate_on_submit():
        donor_file = form.donor_file.data
        donor_file.save(os.path.join(os.path.abspath("app/static/files/"),secure_filename(donor_file.filename)))
        try:
            donorDetails = pd.read_csv(os.path.join(os.path.abspath("app/static/files/"),secure_filename(donor_file.filename)))
            first_name = donorDetails['First Name']
            last_name = donorDetails['Last Name or Initial']
            donor_names = [f"{first.strip()} {last.strip()}" for first, last in zip(first_name, last_name)]
            print(donor_names)
        except Exception as e:
            print(e)
            return render_template('manage_donors_admin.html', form=form)