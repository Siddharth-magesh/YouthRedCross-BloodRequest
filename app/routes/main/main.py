# app/routes/main.py
from flask import Blueprint, render_template
from app.models import QueryTable
from app.utils.data_manipulations_toDB import FetchDetails
import json

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/render_find_donors_page')
def render_find_donors_page():
    return render_template('fetch_donors.html')

@main_bp.route('/render_register_new_donor')
def render_register_new_donor():
    return render_template('register_donor.html')

@main_bp.route('/render_generate_blood_request', methods=['GET', 'POST'])
def render_generate_blood_request():
    try:
        FetchDetails.fetch_hospital_details_autofill()
        with open('app/static/json_files/hospital_details.json', 'r') as file:
            hospitals_data = json.load(file)
    except FileNotFoundError:
        hospitals_data = []

    return render_template('generate_request.html',hospitals_json=hospitals_data)

@main_bp.route('/render_AboutUs_Page')
def render_AboutUs_Page():
    return render_template('aboutus.html')

@main_bp.route('/render_donor_login')
def render_donor_login():
    return render_template('donor_login.html')

@main_bp.route('/render_forget_password_page')
def render_forget_password_page():
    return render_template('forget_password_donor.html')

@main_bp.route('/render_blood_banks_page')
def render_blood_banks_page():
    return render_template('blood_banks.html')

@main_bp.route('/render_forget_password_donor')
def render_forget_password_donor():
    return render_template('forget_password_donor.html')

@main_bp.route('/render_query_page')
def render_query_page():
    queries = QueryTable.query.all()
    return render_template('query_page_donor.html',queries=queries)