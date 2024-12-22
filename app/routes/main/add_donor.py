from flask import Blueprint, render_template, request, flash , redirect , url_for , current_app
from werkzeug.security import generate_password_hash
from app.models import db, PersonalDetailsUser, AddressDetailsUser, DiseaseDetailsUser, AuthenticationDetailsDonor, DonorDetail , TermsAndConditions
from werkzeug.security import check_password_hash
from datetime import datetime
from app.utils.data_manipulations_toDB import FetchDetails
import secrets
import smtplib
from email.mime.text import MIMEText
from app.config import Config

cred = Config()
new_donor = Blueprint('add_donor', __name__)

def generate_secure_numeric_otp(length=6):
    otp = ''.join(str(secrets.randbelow(10)) for _ in range(length))
    return otp

def send_email(subject, recipient, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = cred.BASE_MAIL_ADDRESS
    msg['To'] = recipient

    with smtplib.SMTP(cred.MAIL_SERVER, cred.MAIL_PORT) as server:
        server.starttls() 
        server.login(cred.MAIL_USERNAME, cred.MAIL_PASSWORD)
        server.sendmail(cred.BASE_MAIL_ADDRESS, recipient, msg.as_string())

def get_next_id(table, prefix):
    max_id = db.session.query(table.id).order_by(table.id.desc()).first()
    next_id_num = 1
    if max_id:
        current_num = int(max_id[0][len(prefix):])
        next_id_num = current_num + 1
    return f"{prefix}{str(next_id_num).zfill(3)}"

#used only for generating authentication ID
def get_next_id_secondary_function(table, prefix):
    max_id = db.session.query(table.authentication_id).order_by(table.authentication_id.desc()).first()
    next_id_num = 1
    if max_id:
        current_num = int(max_id[0][len(prefix):])
        next_id_num = current_num + 1
    return f"{prefix}{str(next_id_num).zfill(3)}"

#used only for generating Terms and Conditions ID
def get_next_id_third_function(table, prefix):
    max_id = db.session.query(table.terms_and_conditions_id).order_by(table.terms_and_conditions_id.desc()).first()
    next_id_num = 1
    if max_id:
        current_num = int(max_id[0][len(prefix):])
        next_id_num = current_num + 1
    return f"{prefix}{str(next_id_num).zfill(3)}"

@new_donor.route('/register_new_donors', methods=['GET', 'POST'])
def register_new_donors():
    if request.method == 'POST':
        try:
            # Section 1: Login Credentials
            email = request.form.get('Email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            if password != confirm_password:
                flash('Make sure you enter similar passwords', 'danger')
                return render_template('register_donor.html')

            hashed_password = generate_password_hash(password)

            # Section 2: Personal Details
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name', '')
            name = first_name + ' ' +last_name
            age = request.form.get('age')
            dob = request.form.get('dob')
            contact_number = request.form.get('contact_number')
            secondary_contact = request.form.get('secondary_contact')
            marital_status = request.form.get('marital_status')
            aadhar_number = request.form.get('aadhar_number')
            blood_group = request.form.get('blood_group')
            last_donation = request.form.get('last_donation')
            previous_blood_donation_status = request.form.get('previous_blood_donation_status')
            blood_donation_count = request.form.get('blood_donated_count')

            if previous_blood_donation_status == '0':
                blood_donation_count = '0'
                last_donation=None

            if last_donation == '':
                last_donation=None

            personal_id = get_next_id(PersonalDetailsUser, 'PDDNR')
            personal_details = PersonalDetailsUser(
                id=personal_id,
                first_name=first_name,
                last_name=last_name,
                age=age,
                date_of_birth=dob,
                contact_number=contact_number,
                secondary_contact_number=secondary_contact,
                marital_status=marital_status,
                aadhar_number=str(aadhar_number)
            )
            db.session.add(personal_details)

            # Section 3: Address Details
            address = request.form.get('address')
            city = request.form.get('city')
            state = request.form.get('state')
            pincode = request.form.get('pincode')
            country = request.form.get('country')
            full_address = f"{address}, {city}, {state}, {pincode}".strip()

            address_id = get_next_id(AddressDetailsUser, 'ADDR')
            address_details = AddressDetailsUser(
                id=address_id,
                address=full_address,
                pincode=pincode,
                country=country,
                state=state,
                city=city
            )
            db.session.add(address_details)

            # Section 4: Disease Details
            disease_name = request.form.get('disease_name')
            description = request.form.get('description')

            disease_id = get_next_id(DiseaseDetailsUser, 'DIS')
            disease_details = DiseaseDetailsUser(
                id=disease_id,
                name=disease_name,
                description=description
            )
            db.session.add(disease_details)

            auth_id = get_next_id_secondary_function(DonorDetail, 'AUTHDNR')
            
            # terms and Conditions
            terms_and_conditions_id = get_next_id_third_function(DonorDetail, 'TCDNR')
            term_condtions = TermsAndConditions(
                id = terms_and_conditions_id,
                version = "1.0",
                effective_date = datetime.now()
            )
            db.session.add(term_condtions)

            # Create and add DonorDetail entry
            donor_id = get_next_id(DonorDetail, 'DNR')
            donor_detail = DonorDetail(
                id=donor_id,
                name=name,
                email = email,
                password = hashed_password,
                blood_group = blood_group,
                personal_details_id=personal_id,
                terms_and_conditions_id=terms_and_conditions_id,
                address_id = address_id,
                active_status = True,
                disease_id = disease_id,
                authentication_id = auth_id,
                last_donated_date = last_donation,
                number_of_times_donated = blood_donation_count,
                last_login_date = None
            )
            db.session.add(donor_detail)

            db.session.commit()
            flash('Donor successfully added!', 'success')
            confirmation_details = [
                email,
                name,
                age,
                dob,
                contact_number,
                secondary_contact,
                marital_status,
                aadhar_number,
                blood_group,
                full_address,
                disease_name,
                description
            ]
            return render_template('new_donor_registration_confirmation.html',details = confirmation_details)

        except Exception as e:
            db.session.rollback()
            print(e)
            flash(f'Error adding donor: {e}', 'danger')
            return render_template('register_donor.html')

    return render_template('register_donor.html')

@new_donor.route('/donor_login_validation',methods=['POST','GET'])
def donor_login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    captcha = current_app.extensions.get('captcha')
    if not captcha or not captcha.validate():
        flash("Invalid CAPTCHA. Please try again.", "error")
        return redirect(url_for('main.render_donor_login'))

    donor = DonorDetail.query.filter_by(email=email).first()
    if not donor:
        flash("Email not registered. Please sign up.", "error")
        return redirect(url_for('main_bp.render_donor_login'))
    
    if donor and check_password_hash(donor.password,password):
        current_datetime = datetime.now()
        current_date = current_datetime.date()
        current_time = current_datetime.time()
        donor.last_login_date = current_datetime
        logging_details = AuthenticationDetailsDonor(
            auth_id = donor.authentication_id,
            name = donor.name,
            login_date = current_date,
            login_time = current_time
        )
        db.session.add(logging_details)
        db.session.commit()
        details = FetchDetails.fetch_donor_details(donor.id)
        return render_template('donor_dashboard.html',details = details)
    else:
        return "Invalid email or password", 401
    
@new_donor.route('/modify_donor_details',methods=['POST','GET'])
def modify_donor_details():
    donor_id = request.form.get('id')
    donor = DonorDetail.query.get(donor_id)
    if not donor:
        flash("Donor not found.")
        return "Donor not found", 404
    
    name = request.form.get('name')
    blood_group = request.form.get('blood_group')
    if name and name != donor.name:
        donor.name = name

    if blood_group and blood_group != donor.blood_group:
        donor.blood_group = blood_group
    
    personal_details = PersonalDetailsUser.query.get(donor.personal_details_id)
    if personal_details:
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        age = request.form.get('age')
        contact_number = request.form.get('contact_number')
        secondary_contact_number = request.form.get('secondary_contact_number')
        marital_status = request.form.get('marital_status')
        aadhar_number = request.form.get('aadhar_number')

        if first_name and first_name != personal_details.first_name:
            personal_details.first_name = first_name
        if last_name and last_name != personal_details.last_name:
            personal_details.last_name = last_name
        if age and age != str(personal_details.age):
            personal_details.age = int(age)
        if contact_number and contact_number != personal_details.contact_number:
            personal_details.contact_number = contact_number
        if secondary_contact_number and secondary_contact_number != personal_details.secondary_contact_number:
            personal_details.secondary_contact_number = secondary_contact_number
        if marital_status and marital_status != personal_details.marital_status:
            personal_details.marital_status = marital_status
        if aadhar_number and aadhar_number != personal_details.aadhar_number:
            personal_details.aadhar_number = aadhar_number

    address_details = AddressDetailsUser.query.get(donor.address_id)
    if address_details:
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country')
        pincode = request.form.get('pincode')
        
        if address and address != address_details.address:
            address_details.address = address
        if city and city != address_details.city:
            address_details.city = city
        if state and state != address_details.state:
            address_details.state = state
        if country and country != address_details.country:
            address_details.country = country
        if pincode and pincode != address_details.pincode:
            address_details.pincode = pincode


    disease_details = DiseaseDetailsUser.query.get(donor.disease_id)
    if disease_details:
        disease_name = request.form.get('disease_name')
        disease_description = request.form.get('disease_description')
        
        if disease_name and disease_name != disease_details.name:
            disease_details.name = disease_name
        if disease_description and disease_description != disease_details.description:
            disease_details.description = disease_description
    
    try:
        db.session.commit()
        flash("Donor details updated successfully.")
        confirmation_details = [
            name,
            blood_group,
            first_name,
            last_name,
            age,
            contact_number,
            secondary_contact_number,
            marital_status,
            aadhar_number,
            address, 
            city, 
            state,
            country,
            pincode,
            disease_name,
            disease_description
        ]
        print(confirmation_details)
        return render_template('donor_details_updation_confirmation.html',details = confirmation_details)
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {e}")
        return "An error occurred while updating the donor details", 500
    
@new_donor.route('/manage_forget_password_donor',methods=['POST','GET'])
def manage_forget_password_donor():
    email = request.form.get('email')
    one_time_password = generate_secure_numeric_otp()

    fetched_donor = DonorDetail.query.filter_by(email=email).first()

    if fetched_donor and fetched_donor.email == email:
        subject = "Request for Password Change"
        recipient = email
        link = "http://127.0.0.1:5000/main/render_query_page"
        body = f"""
        Dear User,

        We Have got a Request from your YRC-LBS Account for Changing your password.
        if You haven't generated it , let us Know in the below link
        {link}
        if You have requested for it , use the below OTP to change your password

        One Time Password ! Don't Share it with any third parties !
        {one_time_password}

        Regards,
        Youth Red Cross Blood Donation Site
        """
        send_email(subject, recipient, body)

        return render_template('otp_validation_donor.html',one_time_password=one_time_password,email=email)
    else:
        flash("An error occurred:")
        return "An error occurred while updating the donor details", 500

@new_donor.route('/otp_validation',methods=['POST','GET'])
def otp_validation():
    generate_otp = request.form.get('generated_otp')
    typed_otp = request.form.get('typed_otp')
    email = request.form.get('email')

    if str(generate_otp) == str(typed_otp):
        return render_template('donor_new_password.html',email=email)
    else :
        return "Wrong One Time Password"
    
@new_donor.route('/new_password_donor',methods=['POST','GET'])
def new_password_donor():
    password = request.form.get('password')
    confirmpassword = request.form.get('confirmpassword')
    email = request.form.get('email')

    if password==confirmpassword:
        donor = DonorDetail.query.filter_by(email=email).first()
        hashed_password = generate_password_hash(password)
        donor.password = hashed_password
        db.session.commit()
        return redirect(url_for('main.render_donor_login'))
    else:
        return "Couldnt Update the password"
