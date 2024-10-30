from flask import render_template, Blueprint, request , redirect , url_for , jsonify
from app.database import DonorDetail, db 
from app.config import Config
import smtplib
from email.mime.text import MIMEText
from app.utils.data_manipulations_toDB import FetchDetails

cred = Config()
approveNewRequest = Blueprint('approve_new_requests', __name__)

def send_email(subject, recipient, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = cred.BASE_MAIL_ADDRESS 
    msg['To'] = recipient

    with smtplib.SMTP(cred.MAIL_SERVER, cred.MAIL_PORT) as server:
        server.starttls() 
        server.login(cred.MAIL_USERNAME, cred.MAIL_PASSWORD)
        server.sendmail(cred.BASE_MAIL_ADDRESS, recipient, msg.as_string())

@approveNewRequest.route('/SendEmailToDonors', methods=['POST', 'GET'])
def SendEmailToDonors():
    data = request.get_json()
    request_id = data.get('request_id')
    blood_group = data.get('blood_group')  
    patient_name = data.get('patient_name')
    hospital_name = data.get('hospital_name')
    hospital_address = data.get('hospital_address')
    contact_number = data.get('contact_number')
    due_date = data.get('due_date')
    attendant_name = data.get('attendant_name')
    units_required = data.get('units_required')
    request_reason = data.get('request_reason')
    patient_age = data.get('patient_age')

    active_donors = DonorDetail.query.filter_by(blood_group=blood_group, active_status=True).all()
    donor_names = [donor.name for donor in active_donors]
    donor_emails = [donor.email for donor in active_donors]

    subject = "Urgent Blood Donation Request"
    
    for email, name in zip(donor_emails, donor_names):
        body = f"""
        Dear {name},

        We hope this message finds you well. We are reaching out to you as part of our commitment to 
        ensuring that patients in need of blood transfusions receive timely assistance. 
        We have received a new blood donation request that matches your blood type: {blood_group}.

        Here are the details of the request:
        - Patient Name: {patient_name}
        - Blood Group Needed: {blood_group}
        - Units Required: {units_required}
        - Patient Age: {patient_age}
        - Hospital Name: {hospital_name}
        - Hospital Address: {hospital_address}
        - Contact Number: {contact_number}
        - Attendant Name: {attendant_name}
        - Due Date for Donation: {due_date}
        - Reason for Request: {request_reason}

        Your willingness to donate can make a significant difference in saving a life.
        If you are available and willing to donate, please respond to this email or contact 
        us directly at the information provided below.

        Thank you for your continued support and willingness to help those in need.

        Best regards,
        Youth Red Cross (Team LFB)

        For any inquiries, please contact us at:
        Phone: 9876543210
        Email: yrclifebloodsupport@gmail.com
        """

        send_email(subject, email, body)
    FetchDetails.update_the_new_requests(request_id)

    success = True  # Set to False if the email sending fails
    
    if success:
        # Return success message to JavaScript
        return jsonify({"success": True, "message": "Email requests sent successfully!"})
    else:
        return jsonify({"success": False, "message": "Failed to send email requests."}), 500
