# app/routes/admin.py
import math
import os
from flask import Blueprint, render_template ,request,flash
from flask_wtf import FlaskForm
from wtforms import SubmitField ,FileField
from wtforms.validators import InputRequired
from app.utils.data_manipulations_toDB import FetchDetails
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import pandas as pd
from app.utils.helper import get_next_id,convert_to_date, is_donor_active, replace_none
from app.models import db,PersonalDetailsUser, AddressDetailsUser, DiseaseDetailsUser, AuthenticationDetailsDonor, DonorDetail

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

class AddDonorCSV(FlaskForm):
    new_donor_file = FileField('Donor CSV File', validators=[InputRequired()])
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
        donor_file = form.new_donor_file.data
        donor_file.save(os.path.join(os.path.abspath("app/static/files/"),secure_filename(donor_file.filename)))
        try:
            donorDetails = pd.read_csv(os.path.join(os.path.abspath("app/static/files/"),secure_filename(donor_file.filename)))
            first_name = donorDetails['First Name'].astype(str)
            last_name = donorDetails['Last Name or Initial'].astype(str)
            # details for personal details table
            donor_names = [f"{first.strip()} {last.strip()}" for first, last in zip(first_name, last_name)]
            donor_age = donorDetails['Age'].astype(int)
            donor_dob = convert_to_date(donorDetails['Date of Birth'])
            donor_contact = donorDetails['Phone Number'].astype(int)
            donor_secondary_contact = donorDetails['Secondary Contact Number'].astype(int)
            donor_martial_status = donorDetails['Martial Status'].astype(str)
            donor_aadhar = donorDetails['Aadhar Number'].astype(int)

            # details for address table
            donor_address = donorDetails['Current Address'].astype(str)
            donor_pincode = donorDetails['Pincode'].astype(int)
            donor_city = donorDetails['City'].astype(str)
            donor_state = donorDetails['State'].astype(str)
            donor_country = donorDetails['Country'] if 'Country' in donorDetails.columns else ['India'] * len(donorDetails)
            
            # details for diseases table
            donor_disease = donorDetails['Any Disease or Allergies'].astype(str)
            replaced_disease = [replace_none(str(disease)) for disease in donor_disease]
            donor_disease_details = donorDetails['Disease Description'].astype(str)

            # donor blood details
            donor_blood_group = donorDetails['Blood Group'].astype(str)
            # is_blood_donated = donorDetails['Donated Blood Already']
            donor_last_donation = convert_to_date(donorDetails['Last Blood Donated Date'])
            donor_donation_count = [0 if math.isnan(x) else int(x) for x in donorDetails['No of Times Donated'].tolist()]
            donor_status = is_donor_active(donor_last_donation)

            # donor login details
            donor_email = donorDetails['Email Address'].astype(str)
            donor_password = donorDetails['Password'].astype(str)
            donor_confirm_password = donorDetails['Confirm Password'].astype(str)

            for i in range(len(donor_names)):
                personal_id = get_next_id(PersonalDetailsUser, 'PDDNR')
                personal_details = PersonalDetailsUser(
                    id=personal_id,
                    first_name=first_name[i],
                    last_name=last_name[i],
                    age=donor_age[i],
                    date_of_birth=donor_dob[i],
                    contact_number=donor_contact[i],
                    secondary_contact_number=donor_secondary_contact[i],
                    marital_status=donor_martial_status[i],
                    aadhar_number=donor_aadhar[i]
                )
                address_id = get_next_id(AddressDetailsUser, 'ADDNR')
                address_details = AddressDetailsUser(
                    id=address_id,
                    address=donor_address[i],
                    city=donor_city[i],
                    state=donor_state[i],
                    pincode=donor_pincode[i],
                    country=donor_country[i] if not pd.isnull(donor_country[i]) else 'India'
                )
                disease_id = get_next_id(DiseaseDetailsUser, 'DISNR')
                disease_details = DiseaseDetailsUser(
                    id=disease_id,
                    name=replaced_disease[i],
                    description=donor_disease_details[i]
                )
                auth_id = get_next_id(AuthenticationDetailsDonor, 'AUTHDNR')
                donor_authentication = AuthenticationDetailsDonor(
                    id=auth_id,
                    name = donor_names[i],
                )
                if donor_password[i] == donor_confirm_password[i]:
                    hashed_donor_password = generate_password_hash(donor_password[i],method="scrypt")
                donor_id = get_next_id(AuthenticationDetailsDonor, 'DNR')
                donor_detail = DonorDetail(
                    id = donor_id,
                    name = donor_names[i],
                    email = donor_email[i],
                    password = hashed_donor_password,
                    blood_group = donor_blood_group[i],
                    personal_details_id = personal_id,
                    address_id = address_id,
                    active_status = donor_status[i],
                    disease_id = disease_id,
                    authentication_id = auth_id,
                    last_donated_date = donor_last_donation[i],
                    number_of_times_donated = donor_donation_count[i],
                )
                # personal_id = get_next_id(PersonalDetailsUser, 'PDDNR')
                # address_id = get_next_id(AddressDetailsUser, 'ADDNR')
                # disease_id = get_next_id(DiseaseDetailsUser, 'DISNR')
                db.session.add(personal_details)
                db.session.commit()
                db.session.add(address_details)
                db.session.commit()
                db.session.add(disease_details)
                db.session.commit()
                db.session.add(donor_authentication)
                db.session.commit()
                db.session.add(donor_detail)
                db.session.commit()
        except Exception as e:
            print(e)
    return render_template('add_donors_csv.html', form=form)