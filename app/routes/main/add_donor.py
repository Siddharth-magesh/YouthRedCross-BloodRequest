from flask import Blueprint, render_template, request, flash
from werkzeug.security import generate_password_hash
from app.models import db, PersonalDetailsUser, AddressDetailsUser, DiseaseDetailsUser, AuthenticationDetailsDonor, DonorDetail
from werkzeug.security import check_password_hash
from datetime import datetime
from app.utils.data_manipulations_toDB import FetchDetails

new_donor = Blueprint('add_donor', __name__)

def get_next_id(table, prefix):
    # Fetch the current maximum ID, strip the prefix and convert to an integer
    max_id = db.session.query(table.id).order_by(table.id.desc()).first()
    next_id_num = 1
    if max_id:
        # Extract the numeric part of the ID
        current_num = int(max_id[0][len(prefix):])
        next_id_num = current_num + 1
    # Format the new ID
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

            # Create and add PersonalDetails entry
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
                aadhar_number=aadhar_number
            )
            db.session.add(personal_details)

            # Section 3: Address Details
            address = request.form.get('address')
            city = request.form.get('city')
            state = request.form.get('state')
            pincode = request.form.get('pincode')
            country = request.form.get('country')
            full_address = f"{address}, {city}, {state}, {pincode}".strip()

            # Create and add AddressDetails entry
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

            # Create and add DiseaseDetails entry
            disease_id = get_next_id(DiseaseDetailsUser, 'DIS')
            disease_details = DiseaseDetailsUser(
                id=disease_id,
                name=disease_name,
                description=description
            )
            db.session.add(disease_details)

            # Create and add AuthenticationDetails entry
            auth_id = get_next_id(AuthenticationDetailsDonor, 'AUTHDNR')

            # Create and add DonorDetail entry
            donor_id = get_next_id(DonorDetail, 'DNR')
            donor_detail = DonorDetail(
                id=donor_id,
                name=name,
                email = email,
                password = hashed_password,
                blood_group = blood_group,
                personal_details_id=personal_id,  # Foreign key
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
            return render_template('index.html')

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

    donor = DonorDetail.query.filter_by(email=email).first()
    
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
        return render_template('index.html')
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {e}")
        return "An error occurred while updating the donor details", 500