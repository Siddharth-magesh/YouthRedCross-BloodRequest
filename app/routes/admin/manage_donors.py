from flask import Blueprint , render_template , request , flash , redirect , url_for
from app.utils.data_manipulations_toDB import FetchDetails
from app.models import DonorDetail , PersonalDetailsUser , DiseaseDetailsUser , db , AddressDetailsUser

manage_donors = Blueprint('manageDonor',__name__)

@manage_donors.route('/manage_donor_details',methods=['POST','GET'])
def manage_donor_details():
    donor_id = request.form.get('id')
    donor = DonorDetail.query.get(donor_id)
    if not donor:
        flash("Donor not found.")
        return "Donor not found", 404
    
    name = request.form.get('name')
    blood_group = request.form.get('blood_group')
    if name and name != donor.name:
        donor.name = name

    active_status = request.form.get('active_status')
    if active_status and active_status != str(donor.active_status):
        if active_status=='True':
            donor.active_status = True
        else:
            donor.active_status = False

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
        return redirect(url_for('admin.render_manage_donors_admin_page'))
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {e}")
        return "An error occurred while updating the donor details", 500
