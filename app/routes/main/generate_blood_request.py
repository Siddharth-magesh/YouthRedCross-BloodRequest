from flask import Blueprint, render_template, request , flash , redirect , url_for
from app.models import db, BloodRequestDetails, HospitalDetails, ResponseDetails , AdminDetails
from app.config import Config
import smtplib
from email.mime.text import MIMEText
import os
import csv

cred = Config() 
generate_blood_request = Blueprint('generate_blood_request', __name__)

def send_email(subject, recipient, body):
    msg = MIMEText(body,"html")
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

@generate_blood_request.route('/generate_bloodRequest', methods=['POST', 'GET'])
def generate_bloodRequest():
    if request.method == 'POST':
        CSV_FILE = r'D:\YouthRedCross-BloodRequest\docs\requestdata.csv'
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

        #Replace the below code before going into production
        headers = [
            "Patient Name", "Attendant Name", "Blood Group", "Hospital ID", "Hospital Name",
            "Contact Number", "Patient Age", "Hospital Address", "Pincode", "Landmark",
            "Due Date", "Request Reason", "Units Required"
        ]
        data_row = [
            patient_name, attendant_name, blood_group, hospital_id, hospital_name,
            contact_number, patient_age, hospital_address, pincode, landmark,
            due_date, request_reason, units_required
        ]
        file_exists = os.path.isfile(CSV_FILE)
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(headers)
            writer.writerow(data_row)

        flash("Blood request generated successfully!", "success")
        return redirect(url_for('main.index'))
        #Remove till here

        if hospital_id in [None, '', 'None']: 
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
            response_id=response_id
        )

        db.session.add(blood_request)
        db.session.commit()

        active_admins = AdminDetails.query.filter_by(active_status='Active').all()
        active_admin_emails = [admin.email for admin in active_admins]

        for admin_email in active_admin_emails:
            subject = "New Blood Request Generated"
            recipient = admin_email
            link = "http://127.0.0.1:5000/admin/render_admin_login" 
            body = f"""
            <html>
                <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
                    <table align="center" width="600" style="margin: 20px auto; border-collapse: collapse; background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                        <!-- Header -->
                        <tr>
                            <td style="background-color: #8B0000; padding: 20px; text-align: center; border-top-left-radius: 8px; border-top-right-radius: 8px;">
                                <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: bold;">Blood Request Notification</h1>
                            </td>
                        </tr>
                        <!-- Content -->
                        <tr>
                            <td style="padding: 30px; color: #333;">
                                <p style="font-size: 18px; margin: 0 0 15px;">Dear Admin,</p>
                                <p style="font-size: 16px; margin: 0 0 20px; line-height: 1.6;">
                                    This is to inform you that a new <strong style="color: #8B0000;">blood request</strong> has been initiated and requires your immediate attention. 
                                </p>
                                <p style="font-size: 16px; margin: 0 0 20px; line-height: 1.6;">
                                    Kindly review and process the request at your earliest convenience by accessing the link provided below.
                                </p>
                                <p style="text-align: center;">
                                    <a href="{link}" style="display: inline-block; font-size: 16px; text-decoration: none; color: white; background-color: #8B0000; padding: 15px 25px; border-radius: 5px; font-weight: bold;">
                                        Review Request
                                    </a>
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
                                    © 2024 LifeConnect Donation Team. All rights reserved.
                                </p>
                            </td>
                        </tr>
                    </table>
                </body>
            </html>
            """

            send_email(subject, recipient, body)

        confirmation_details = [
            patient_name,blood_group,hospital_name,contact_number,hospital_address,
        ]

        return render_template('bloodrequest_confirmation.html',details = confirmation_details)

    return render_template('generate_blood_request.html')
