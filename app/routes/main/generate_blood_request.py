from flask import Blueprint, render_template, request
from app.database import db, BloodRequestDetails, HospitalDetails, ResponseDetails  # Import your database session

generate_blood_request = Blueprint('generate_blood_request', __name__)

def get_next_id(table, prefix):
    max_id = db.session.query(table.id).order_by(table.id.desc()).first()
    next_id_num = 1
    if max_id:
        current_num = int(max_id[0][len(prefix):])
        next_id_num = current_num + 1
    return f"{prefix}{str(next_id_num).zfill(3)}"

@generate_blood_request.route('/generate_bloodRequest', methods=['POST', 'GET'])
def generate_bloodRequest():
    if request.method == 'POST':
        # Fetch values from the form
        patient_name = request.form.get('patient_name')
        attendant_name = request.form.get('attendant_name')
        blood_group = request.form.get('blood_group')
        hospital_id = request.form.get('hospital_id')
        hospital_name = request.form.get('hospital_name')
        contact_number = request.form.get('contact_number')
        patient_age = request.form.get('patient_age')
        hospital_address = request.form.get('hospital_address')
        pincode = request.form.get('pincode')
        landmark = request.form.get('landmark')
        due_date = request.form.get('due_date')
        request_reason = request.form.get('request_reason')
        units_required = request.form.get('units_required')

        print(hospital_id)
        # Ensure hospital_id is properly checked
        if hospital_id in [None, '', 'None']:  # Check for None, empty string, and string 'None'
            new_hospital_id = get_next_id(HospitalDetails, 'HOSP')
            new_hospital = HospitalDetails(
                id=new_hospital_id,
                hospital_name=hospital_name,
                hospital_address=hospital_address,
                pincode=pincode,
                city='Chennai',
                state='Tamil Nadu',
                country='India',
                branch=None,
                landmark=None
            )
            db.session.add(new_hospital)
            db.session.commit()  # Commit the new hospital to generate its ID
            print("Added Hospital")
            hospital_id = new_hospital_id  # Assign the new hospital's ID to hospital_id
            print(hospital_id)

        # Create and commit a new ResponseDetails entry to get a valid response_id
        response_id = get_next_id(ResponseDetails, 'RESP')
        response = ResponseDetails(
            id=response_id,
            status='Pending',
            report=None,
            units_donated=None,
            donor_ids=None
        )
        db.session.add(response)
        db.session.commit()  # Commit to ensure response_id is available
        print("created response column")

        # Proceed with creating the blood request
        bloodrequest_id = get_next_id(BloodRequestDetails, 'BR')
        print("hosiptal id : ",hospital_id)
        blood_request = BloodRequestDetails(
            id=bloodrequest_id,
            patient_name=patient_name,
            attendant_name=attendant_name,
            blood_group=blood_group,
            hospital_id=hospital_id,  # Use hospital_id here
            hospital_name=hospital_name,
            contact_number=contact_number,
            patient_age=patient_age,
            due_date=due_date,
            request_reason=request_reason,
            units_required=units_required,
            status='Pending',
            donor_ids=None,
            response_id=response_id  # Use the committed response_id
        )

        db.session.add(blood_request)
        db.session.commit()

        return "Success"

    return render_template('generate_blood_request.html')
