from flask import Blueprint , render_template , request , flash ,redirect , url_for
from app.models import HospitalDetails , db

manage_hospital = Blueprint('manage_hospital',__name__)

@manage_hospital.route('/modify_hospital_details',methods=['POST','GET'])
def modify_hospital_details():
    hospital_id = request.form.get('id')
    hospital_name = request.form.get('hospital_name')
    hospital_address = request.form.get('hospital_address')
    city = request.form.get('city')
    state = request.form.get('state')
    country = request.form.get('country')
    pincode = request.form.get('pincode')
    branch = request.form.get('branch')
    landmark = request.form.get('landmark')

    hospital_details = HospitalDetails.query.get(hospital_id)

    if hospital_details:
        if hospital_name and hospital_name != HospitalDetails.hospital_name:
            hospital_details.hospital_name = hospital_name

        if hospital_address and hospital_address != HospitalDetails.hospital_address:
            hospital_details.hospital_address = hospital_address

        if pincode and pincode != HospitalDetails.pincode:
            hospital_details.pincode = pincode

        if city and city != HospitalDetails.city:
            hospital_details.city = city

        if state and state != HospitalDetails.state:
            hospital_details.state = state

        if country and country != HospitalDetails.country:
            hospital_details.country = country

        if branch and branch != HospitalDetails.branch:
            hospital_details.branch = branch

        if landmark and landmark != HospitalDetails.landmark:
            hospital_details.landmark = landmark

    try:
        db.session.commit()
        flash("Hospital details updated successfully.")
        return redirect(url_for('admin.render_hospital_details_admin'))
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {e}")
        return "An error occurred while updating the donor details", 500