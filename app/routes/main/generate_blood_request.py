from flask import Blueprint, render_template, request
from app.models import db, BloodRequestDetails, HospitalDetails, ResponseDetails
from app.config import Config
import smtplib
from email.mime.text import MIMEText

cred = Config()  # Configuration instance
generate_blood_request = Blueprint('generate_blood_request', __name__)

def send_email(subject, recipient, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = cred.BASE_MAIL_ADDRESS  # Use cred instead of current_app.config
    msg['To'] = recipient

    # Connect to the email server
    with smtplib.SMTP(cred.MAIL_SERVER, cred.MAIL_PORT) as server:
        server.starttls()  # Secure the connection
        server.login(cred.MAIL_USERNAME, cred.MAIL_PASSWORD)
        server.sendmail(cred.BASE_MAIL_ADDRESS, recipient, msg.as_string())

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
            db.session.commit() 

            hospital_id = new_hospital_id  

        response_id = get_next_id(ResponseDetails, 'RESP')
        response = ResponseDetails(
            id=response_id,
            status='Not_Approved',
            report=None,
            units_donated=None,
            donor_ids=None
        )
        db.session.add(response)
        db.session.commit()

        # Proceed with creating the blood request
        bloodrequest_id = get_next_id(BloodRequestDetails, 'BR')
        blood_request = BloodRequestDetails(
            id=bloodrequest_id,
            patient_name=patient_name,
            attendant_name=attendant_name,
            blood_group=blood_group,
            hospital_id=hospital_id,
            hospital_name=hospital_name,
            contact_number=contact_number,
            patient_age=patient_age,
            due_date=due_date,
            request_reason=request_reason,
            units_required=units_required,
            status='Not_Approved',
            donor_ids=None,
            response_id=response_id
        )

        db.session.add(blood_request)
        db.session.commit()

        # Send email notification to admin
        subject = "New Blood Request Generated"
        recipient = cred.ADMIN_MAIL_ADDRESS
        link = "http://127.0.0.1:5000/admin/render_admin_login"  # Placeholder link
        body = f"""
        Dear Admin,

        A new blood request has been generated and is pending your authorization.
        Please review the request at the following link:

        {link}

        Regards,
        Youth Red Cross Blood Donation Site
        """
        send_email(subject, recipient, body)

        return render_template('bloodrequest_confirmation.html')

    return render_template('generate_blood_request.html')
