# app/routes/admin.py
import math
import os
from flask import Blueprint, render_template ,request,flash, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField ,FileField
from wtforms.validators import InputRequired
from app.utils.data_manipulations_toDB import FetchDetails
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import pandas as pd
from app.utils.helper import get_next_id, convert_to_date, is_donor_active, replace_none, get_next_id_secondary_function
from app.models import db,PersonalDetailsUser, AddressDetailsUser, DiseaseDetailsUser, AuthenticationDetailsDonor, DonorDetail

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def check_admin_login():
    if session.get('logged_in'):
        return True
    return False

class AddDonorCSV(FlaskForm):
    new_donor_file = FileField('Donor CSV File', validators=[InputRequired()])
    submit = SubmitField('Upload')

@admin_bp.route('/render_admin_login')
def render_admin_login():
    if not session.get('logged_in'):
        return render_template('admin_login.html')
    return redirect(url_for('admin.render_main_admin_page'))

@admin_bp.route('/render_admin_signup')
def render_admin_signup():
    return render_template('admin_signup.html')

@admin_bp.route('/render_main_admin_page')
def render_main_admin_page():
    if check_admin_login():
        data = FetchDetails.generate_notifications()
        name = session.get('admin_name')
        return render_template('admin_dashboard.html',notifications = data,admin_name=name)
    else:
        return redirect(url_for('admin.render_admin_login'))

@admin_bp.route('/render_new_requests_page')
def render_new_requests_page():
    if check_admin_login():
        requests = FetchDetails.get_new_requests()
        return render_template('new_requests_admin.html',requests = requests)
    else:
        return redirect(url_for('admin.render_admin_login'))

@admin_bp.route('/render_request_approval_confirmation')
def render_request_approval_confirmation():
    if check_admin_login():
        return render_template('request_approval_confirmation.html')
    else:
        return redirect(url_for('admin.render_admin_login'))

@admin_bp.route('/render_ongoing_requests_page')
def render_ongoing_requests_page():
    if check_admin_login():
        requests = FetchDetails.fetch_ongoing_requests()
        return render_template('ongoing_requests_admin.html',requests = requests)
    else:
        return redirect(url_for('admin.render_admin_login'))

@admin_bp.route('/render_closed_requests_page')
def render_closed_requests_page():
    if check_admin_login():
        requests = FetchDetails.fetch_closed_requests()
        return render_template('closed_requests_admin.html',requests = requests)
    else:
        return redirect(url_for('admin.render_admin_login'))

@admin_bp.route('/render_expired_requests_page')
def render_expired_requests_page():
    if check_admin_login():
        requests = FetchDetails.fetch_expired_requests()
        return render_template('expired_requests_admin.html',requests = requests)
    else:
        return redirect(url_for('admin.render_admin_login'))

@admin_bp.route('/render_declined_requests_page')
def render_declined_requests_page():
    if check_admin_login():
        requests = FetchDetails.fetch_declined_requests()
        return render_template('declined_requests_admin.html',requests = requests)
    else:
        return redirect(url_for('admin.render_admin_login'))

@admin_bp.route('/render_analytics_page')
def render_analytics_page():
    if check_admin_login():
        data = FetchDetails.generate_analytics()
        return render_template(
            'analytics_admin.html',
            hospital_count=data['hospital_count'],
            recent_donor_count=data['recent_donor_count'],
            recent_request_count=data['recent_request_count']
        )
    else:
        return redirect(url_for('admin.render_admin_login'))

@admin_bp.route('/render_manage_donors_admin_page')
def render_manage_donors_admin_page():
    if check_admin_login():
        donors = FetchDetails.fetch_all_donors()
        return render_template('manage_donors_admin.html',donors=donors)
    else:
        return redirect(url_for('admin.render_admin_login'))

@admin_bp.route('/render_donor_modification_page',methods=['POST','GET'])
def render_donor_modification_page():
    if check_admin_login():
        donor_id = request.form.get('donor_id')
        details = FetchDetails.fetch_donor_details(donor_id)
        return render_template('manage_each_donor_admin.html',details=details)
    else:
        return redirect(url_for('admin.render_admin_login'))

@admin_bp.route('/render_forget_password_admin')
def render_forget_password_admin():
    return render_template('forget_password_admin.html')

@admin_bp.route('/render_hospital_details_admin')
def render_hospital_details_admin():
    if check_admin_login():
        datas = FetchDetails.fetch_all_hospitals()
        return render_template('manage_hospital_details.html',datas=datas)
    else:
        return redirect(url_for('admin.render_admin_login'))

@admin_bp.route('/render_hospital_modification',methods=['POST','GET'])
def render_hospital_modification():
    if check_admin_login():
        hospital_id = request.form.get('id')
        details = FetchDetails.fetch_hospital_detail(hospital_id)
        return render_template('manage_each_hospital_admin.html',details=details)
    else:
        return redirect(url_for('admin.render_admin_login'))

@admin_bp.route('/render_add_new_hospital')
def render_add_new_hospital():
    if check_admin_login():
        return render_template('add_new_hospital.html')
    else:
        return redirect(url_for('admin.render_admin_login'))

@admin_bp.route('/render_generate_certificate')
def render_generate_certificate():
    if check_admin_login():
        return render_template('generate_certificate.html')
    else:
        return redirect(url_for('admin.render_admin_login'))

@admin_bp.route('/render_admin_profile_page')
def render_admin_profile_page():
    if check_admin_login():
        admin_id = session.get('admin_id')
        details = FetchDetails.fetch_admin_details(admin_id)
        return render_template('admin_profile.html',details=details)
    else:
        return redirect(url_for('admin.render_admin_login'))

@admin_bp.route('/admin_logout')
def admin_logout():
    session.clear()
    return redirect(url_for('main.index'))

@admin_bp.route('/add_donor_csv', methods=['POST','GET'])
def add_donor_csv():
    if check_admin_login():
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
                    address_id = get_next_id(AddressDetailsUser, 'ADDR')
                    address_details = AddressDetailsUser(
                        id=address_id,
                        address=donor_address[i],
                        city=donor_city[i],
                        state=donor_state[i],
                        pincode=donor_pincode[i],
                        country=donor_country[i] if not pd.isnull(donor_country[i]) else 'India'
                    )
                    disease_id = get_next_id(DiseaseDetailsUser, 'DIS')
                    disease_details = DiseaseDetailsUser(
                        id=disease_id,
                        name=replaced_disease[i],
                        description=donor_disease_details[i]
                    )
                    auth_id = get_next_id_secondary_function(DonorDetail, 'AUTHDNR')
                    '''donor_authentication = AuthenticationDetailsDonor(
                        auth_id=auth_id,
                        name = donor_names[i],
                    )'''
                    if donor_password[i] == donor_confirm_password[i]:
                        hashed_donor_password = generate_password_hash(donor_password[i],method="scrypt")
                    donor_id = get_next_id(DonorDetail, 'DNR')
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
                    db.session.add(personal_details)
                    db.session.commit()
                    db.session.add(address_details)
                    db.session.commit()
                    db.session.add(disease_details)
                    db.session.commit()
                    #db.session.add(donor_authentication)
                    #db.session.commit()
                    db.session.add(donor_detail)
                    db.session.commit()
                    flash("Donor Details Added Successfully")
            except Exception as e:
                flash(e)
        return render_template('add_donors_csv.html', form=form)
    else:
        return redirect(url_for('admin.render_admin_login'))