from flask import Blueprint, render_template, request, flash
from werkzeug.security import generate_password_hash
from app.database import db, PersonalDetailsUser, AddressDetailsUser, DiseaseDetailsUser, AuthenticationDetailsDonor, DonorDetail

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
            auth_details = AuthenticationDetailsDonor(
                id=auth_id,
                name=name,
                login_date=None,
                login_time=None
            )
            db.session.add(auth_details)

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
                last_donated_date = last_donation
            )
            db.session.add(donor_detail)

            # Commit transaction
            db.session.commit()
            flash('Donor successfully added!', 'success')
            return render_template('index.html')

        except Exception as e:
            db.session.rollback()
            flash(f'Error adding donor: {e}', 'danger')
            return render_template('register_donor.html')

    return render_template('register_donor.html')
