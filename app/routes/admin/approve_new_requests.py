from flask import render_template, Blueprint, request , redirect , url_for , jsonify
from app.models import DonorDetail, db 
from app.config import Config
import smtplib
from email.mime.text import MIMEText
from app.utils.data_manipulations_toDB import FetchDetails

cred = Config()
approveNewRequest = Blueprint('approve_new_requests', __name__)

def send_email(subject, recipient, body):
    msg = MIMEText(body,"html")
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
        <html>
            <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
                <table align="center" width="600" style="margin: 20px auto; border-collapse: collapse; background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="background-color: #8B0000; padding: 20px; text-align: center; border-top-left-radius: 8px; border-top-right-radius: 8px;">
                            <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: bold;">Urgent Blood Donation Request</h1>
                        </td>
                    </tr>
                    <!-- Content -->
                    <tr>
                        <td style="padding: 30px; color: #333;">
                            <p style="font-size: 18px; margin: 0 0 15px;">Dear {name},</p>
                            <p style="font-size: 16px; margin: 0 0 20px; line-height: 1.6;">
                                We hope this message finds you well. We are reaching out to you as part of our ongoing efforts to ensure timely assistance for patients in need of blood transfusions.
                                We have identified a new blood donation request that matches your blood type: <strong style="color: #8B0000;">{blood_group}</strong>.
                            </p>
                            <p style="font-size: 16px; margin: 0 0 15px; font-weight: bold;">Request Details:</p>
                            <table style="width: 100%; font-size: 16px; color: #333; margin-bottom: 20px;">
                                <tr><td style="padding: 5px; font-weight: bold;">Patient Name:</td><td style="padding: 5px;">{patient_name}</td></tr>
                                <tr><td style="padding: 5px; font-weight: bold;">Blood Group Needed:</td><td style="padding: 5px;">{blood_group}</td></tr>
                                <tr><td style="padding: 5px; font-weight: bold;">Units Required:</td><td style="padding: 5px;">{units_required}</td></tr>
                                <tr><td style="padding: 5px; font-weight: bold;">Patient Age:</td><td style="padding: 5px;">{patient_age}</td></tr>
                                <tr><td style="padding: 5px; font-weight: bold;">Hospital Name:</td><td style="padding: 5px;">{hospital_name}</td></tr>
                                <tr><td style="padding: 5px; font-weight: bold;">Hospital Address:</td><td style="padding: 5px;">{hospital_address}</td></tr>
                                <tr><td style="padding: 5px; font-weight: bold;">Contact Number:</td><td style="padding: 5px;">{contact_number}</td></tr>
                                <tr><td style="padding: 5px; font-weight: bold;">Attendant Name:</td><td style="padding: 5px;">{attendant_name}</td></tr>
                                <tr><td style="padding: 5px; font-weight: bold;">Due Date for Donation:</td><td style="padding: 5px;">{due_date}</td></tr>
                                <tr><td style="padding: 5px; font-weight: bold;">Reason for Request:</td><td style="padding: 5px;">{request_reason}</td></tr>
                            </table>
                            <p style="font-size: 16px; margin: 0 0 20px; line-height: 1.6;">
                                If you are willing and available to donate, we kindly request you to respond at the earliest to facilitate this urgent need. 
                                You may either reach out to one of our <strong>LifeConnect administrators</strong> via phone at <strong>9150450401</strong> or contact the attendant directly using the provided contact information.
                            </p>
                            <p style="font-size: 16px; margin: 0 0 20px; line-height: 1.6;">
                                Your generous contribution can make a significant impact in saving lives, and we deeply value your support in this endeavor.
                            </p>
                        </td>
                    </tr>
                    <!-- Footer -->
                    <tr>
                        <td style="padding: 20px; text-align: center; background-color: #f8f9fa; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px; font-size: 14px; color: #555;">
                            <p style="margin: 0;">
                                Best regards,<br>
                                <strong>LifeConnect Team</strong>
                            </p>
                            <p style="margin: 10px 0 0; font-size: 12px; color: #888;">
                                For any additional inquiries, please contact us at:<br>
                                <strong>Phone:</strong> 9150450401<br>
                                <strong>Email:</strong> yrclifeconnect@gmail.com
                            </p>
                        </td>
                    </tr>
                </table>
            </body>
        </html>
        """


        send_email(subject, email, body)
    FetchDetails.update_the_new_requests(request_id)
    success = True 
    
    if success:
        return jsonify({"success": True, "message": "Email requests sent successfully!"})
    else:
        return jsonify({"success": False, "message": "Failed to send email requests."}), 500


@approveNewRequest.route('/decline_request', methods=['POST', 'GET'])
def decline_request():
    data = request.get_json()
    if not data or 'request_id' not in data:
        return jsonify({"success": False, "message": "Invalid request data"}), 400

    request_id = data.get('request_id')
    success, message = FetchDetails.Decline_new_requests(request_id)
    
    if success:
        return jsonify({"success": True, "message": message})
    else:
        return jsonify({"success": False, "message": message}), 500
