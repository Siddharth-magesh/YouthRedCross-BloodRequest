from flask import render_template , Blueprint , request 
from app.utils.data_manipulations_toDB import FetchDetails
from app.models import DonorDetail , db , BloodRequestDetails
from app.utils.certificate_generation import generate_certificate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from app.config import Config
import os
from datetime import datetime

cred = Config()
closing_requests = Blueprint('close_request',__name__)

def send_email(subject, recipient, body, attachment_path):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = cred.BASE_MAIL_ADDRESS
    msg['To'] = recipient

    msg.attach(MIMEText(body,"html"))

    with open(attachment_path, 'rb') as attachment:
        mime_base = MIMEBase('application', 'octet-stream')
        mime_base.set_payload(attachment.read())
        encoders.encode_base64(mime_base)
        mime_base.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')
        msg.attach(mime_base)

    with smtplib.SMTP(cred.MAIL_SERVER, cred.MAIL_PORT) as server:
        server.starttls()
        server.login(cred.MAIL_USERNAME, cred.MAIL_PASSWORD)
        server.sendmail(cred.BASE_MAIL_ADDRESS, recipient, msg.as_string())
    #print("Email sent with attachment")

@closing_requests.route('/close_expired_requests',methods = ['POST','GET'])
def close_expired_requests():
    if request.method == 'POST':
        request_id = request.form.get('request_id')
        response_status = request.form.get('response_status')
        report = request.form.get('report')
        units_donated = request.form.get('units_donated')
        certificate_status = request.form.get('certificate_status')
        donation_date = request.form.get('donation_date')
        response_donor_ids = request.form.get('response_donor_ids')

        if donation_date=='':
            donation_date=None

        donor_id_list = response_donor_ids.split(',') if response_donor_ids else []
        
        FetchDetails.update_expired_request(
            request_id=request_id,
            response_status=response_status,
            report=report,
            units_donated=units_donated,
            certificate_status=certificate_status,
            donation_date=donation_date,
            response_donor_ids=response_donor_ids
        )

        if str(response_donor_ids) != 'None':
            for donor_id in donor_id_list:
                donor_detail = db.session.query(DonorDetail).filter(DonorDetail.id==donor_id).first()
                if donor_detail:
                    donor_detail.active_status=False
                    donor_detail.last_donated_date=datetime.now()
                    donor_detail.number_of_times_donated = donor_detail.number_of_times_donated + 1
                    db.session.commit()
        
        confirmation_details = [
            request_id,
            response_status,
            report,
            units_donated,
            certificate_status,
            donation_date,
            response_donor_ids
        ]
        return render_template('expired_requests_updation_confirmation.html',details = confirmation_details)
    return render_template('index.html')

@closing_requests.route('/close_ongoing_requests',methods = ['POST','GET'])
def close_ongoing_requests():
    if request.method == 'POST':
        request_id = request.form.get('request_id')
        response_status = request.form.get('response_status')
        report = request.form.get('report')
        units_donated = request.form.get('units_donated')
        certificate_status = request.form.get('certificate_status')
        donation_date = request.form.get('donation_date')
        response_donor_ids = request.form.get('response_donor_ids')

        if donation_date=='':
            donation_date=None

        donor_id_list = response_donor_ids.split(',') if response_donor_ids else []

        FetchDetails.update_ongoing_request(
            request_id=request_id,
            response_status=response_status,
            report=report,
            units_donated=units_donated,
            certificate_status=certificate_status,
            donation_date=donation_date,
            response_donor_ids=response_donor_ids
        )

        if str(response_donor_ids) != 'None':
            for donor_id in donor_id_list:
                donor_detail = db.session.query(DonorDetail).filter(DonorDetail.id==donor_id).first()
                if donor_detail:
                    donor_detail.active_status=False
                    donor_detail.last_donated_date=datetime.now()
                    donor_detail.number_of_times_donated = donor_detail.number_of_times_donated + 1
                    db.session.commit()

        confirmation_details = [
            request_id,
            response_status,
            report,
            units_donated,
            certificate_status,
            response_donor_ids,
            donation_date
        ]
        return render_template('ongoing_requests_updation_confirmation.html',details = confirmation_details)
    return render_template('index.html')

@closing_requests.route('/close_ongoing_requests_and_send_certificates', methods=['POST', 'GET'])
def close_ongoing_requests_and_send_certificates():
    if request.method == 'POST':
        request_id = request.form.get('request_id')
        response_status = request.form.get('response_status')
        report = request.form.get('report')
        units_donated = request.form.get('units_donated')
        certificate_status = request.form.get('certificate_status')
        donation_date = request.form.get('donation_date')
        response_donor_ids = request.form.get('response_donor_ids')

        if donation_date == '':
            return "Enter the Donation date"

        donor_id_list = response_donor_ids.split(',') if response_donor_ids else []
        if str(response_donor_ids) == 'None':
            return "Havent entered any Donor Id"
        
        FetchDetails.update_ongoing_request(
            request_id=request_id,
            response_status=response_status,
            report=report,
            units_donated=units_donated,
            certificate_status=certificate_status,
            donation_date=donation_date,
            response_donor_ids=response_donor_ids
        )

        for donor_id in donor_id_list:
            donor_details = (
                db.session.query(
                    DonorDetail
                )
                .filter(DonorDetail.id == donor_id)
                .first()
            )
            hospital_details = (
                db.session.query(
                    BloodRequestDetails.hospital_name
                )
                .filter(BloodRequestDetails.id==request_id)
                .first()
            )
            donor_name = donor_details.name
            donor_email = donor_details.email
            donor_details.last_donated_date = datetime.now()
            donor_details.active_status=False
            donor_details.number_of_times_donated = donor_details.number_of_times_donated + 1
            donation_date = str(datetime.now().date())
            db.session.commit()
            blood_group = donor_details.blood_group
            location = hospital_details.hospital_name
            certificate_path = generate_certificate(donor_name,donation_date,blood_group,location)
            subject = "Your Blood Donation Certificate"
            body = f"""
            <!DOCTYPE html>
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; background-color: #f9f9f9; margin: 0; padding: 0;">
                <div style="background-color: #ffffff; margin: 20px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; max-width: 600px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                    <div style="background-color: #8B0000; color: white; padding: 15px; text-align: center; border-radius: 8px 8px 0 0; font-size: 20px; font-weight: bold;">
                        LifeConnect - Certificate of Gratitude
                    </div>
                    <div style="padding: 20px; font-size: 16px; color: #333;">
                        <p>Dear <strong>{donor_name}</strong>,</p>
                        
                        <p>
                            On behalf of the entire LifeConnect Team, we extend our heartfelt gratitude for your selfless blood donation.
                            Your contribution has made a profound impact, and your generosity exemplifies the true spirit of compassion and service.
                        </p>
                        
                        <p>
                            As a token of our appreciation, we have <strong>attached your donation certificate below</strong>. We hope it serves as a meaningful reminder
                            of the lives you have helped and the difference you continue to make in our community.
                        </p>
                        
                        <p>
                            Thank you once again for your unwavering support and commitment to saving lives.
                        </p>
                    </div>
                    <div style="font-size: 14px; color: #555; text-align: center; margin-top: 20px;">
                        <p>For any inquiries, please feel free to reach out to us:</p>
                        <p><strong>Phone:</strong> 9150450401</p>
                        <p><strong>Email:</strong> yrclifeconnect@gmail.com</p>
                    </div>
                </div>
            </body>
            </html>
            """

            send_email(subject, donor_email, body, certificate_path)
        
        confirmation_details = [
            request_id,
            response_status,
            report,
            units_donated,
            certificate_status,
            response_donor_ids,
            donation_date
        ]
        return render_template('ongoing_requests_updation_confirmation.html',details = confirmation_details)
    return render_template('index.html')


@closing_requests.route('/close_expired_requests_and_send_certificates', methods=['POST', 'GET'])
def close_expired_requests_and_send_certificates():
    if request.method == 'POST':
        request_id = request.form.get('request_id')
        response_status = request.form.get('response_status')
        report = request.form.get('report')
        units_donated = request.form.get('units_donated')
        certificate_status = request.form.get('certificate_status')
        donation_date = request.form.get('donation_date')
        response_donor_ids = request.form.get('response_donor_ids')

        if donation_date == '':
            return "Enter the Donation date"

        donor_id_list = response_donor_ids.split(',') if response_donor_ids else []
        if str(response_donor_ids) == 'None':
            return "Havent entered any Donor Id"

        donor_id_list = response_donor_ids.split(',') if response_donor_ids else []
        FetchDetails.update_expired_request(
            request_id=request_id,
            response_status=response_status,
            report=report,
            units_donated=units_donated,
            certificate_status=certificate_status,
            donation_date=donation_date,
            response_donor_ids=response_donor_ids
        )

        if str(response_donor_ids) == 'None':
            return "Havent entered any Donor Id"
        
        for donor_id in donor_id_list:
            donor_details = (
                db.session.query(
                    DonorDetail
                )
                .filter(DonorDetail.id == donor_id)
                .first()
            )
            hospital_details = (
                db.session.query(
                    BloodRequestDetails.hospital_name
                )
                .filter(BloodRequestDetails.id==request_id)
                .first()
            )
            donor_name = donor_details.name
            donor_email = donor_details.email
            donor_details.last_donated_date = datetime.now()
            donor_details.active_status=False
            donor_details.number_of_times_donated = donor_details.number_of_times_donated + 1
            donation_date = str(datetime.now().date())
            db.session.commit()
            blood_group = donor_details.blood_group
            location = hospital_details.hospital_name
            certificate_path = generate_certificate(donor_name,donation_date,blood_group,location)
            subject = "Your Blood Donation Certificate"

            body = f"""
            <!DOCTYPE html>
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; background-color: #f9f9f9; margin: 0; padding: 0;">
                <div style="background-color: #ffffff; margin: 20px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; max-width: 600px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                    <div style="background-color: #8B0000; color: white; padding: 15px; text-align: center; border-radius: 8px 8px 0 0; font-size: 20px; font-weight: bold;">
                        LifeConnect - Certificate of Gratitude
                    </div>
                    <div style="padding: 20px; font-size: 16px; color: #333;">
                        <p>Dear <strong>{donor_name}</strong>,</p>
                        
                        <p>
                            On behalf of the entire LifeConnect Team, we extend our heartfelt gratitude for your selfless blood donation.
                            Your contribution has made a profound impact, and your generosity exemplifies the true spirit of compassion and service.
                        </p>
                        
                        <p>
                            As a token of our appreciation, we have <strong>attached your donation certificate below</strong>. We hope it serves as a meaningful reminder
                            of the lives you have helped and the difference you continue to make in our community.
                        </p>
                        
                        <p>
                            Thank you once again for your unwavering support and commitment to saving lives.
                        </p>
                    </div>
                    <div style="font-size: 14px; color: #555; text-align: center; margin-top: 20px;">
                        <p>For any inquiries, please feel free to reach out to us:</p>
                        <p><strong>Phone:</strong> 9150450401</p>
                        <p><strong>Email:</strong> yrclifeconnect@gmail.com</p>
                    </div>
                </div>
            </body>
            </html>
            """


            send_email(subject, donor_email, body, certificate_path)

        confirmation_details = [
            request_id,
            response_status,
            report,
            units_donated,
            certificate_status,
            donation_date,
            response_donor_ids
        ]
        return render_template('expired_requests_updation_confirmation.html',details = confirmation_details)
    return render_template('index.html')