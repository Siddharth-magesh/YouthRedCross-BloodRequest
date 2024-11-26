from flask import Blueprint , render_template , request , flash , redirect , url_for , session
from app.utils.data_manipulations_toDB import FetchDetails
from app.models import DonorDetail , PersonalDetailsUser , DiseaseDetailsUser , db , AddressDetailsUser , QueryTable
from app.utils.certificate_generation import generate_certificate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from datetime import date
from app.config import Config
import os

cred = Config()
manage_donors = Blueprint('manageDonor',__name__)

def send_email(subject, recipient, body, attachment_path):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = cred.BASE_MAIL_ADDRESS
    msg['To'] = recipient

    msg.attach(MIMEText(body, 'plain'))

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
    
@manage_donors.route('/generate_and_send_certificate',methods=['POST','GET'])
def generate_and_send_certificate():
    donor_name = request.form.get('donor_name')
    donor_email = request.form.get('donor_email')
    donation_date = request.form.get('donation_date')
    blood_group = request.form.get('blood_group')
    location = request.form.get('location')
    certificate_path = generate_certificate(donor_name,donation_date,blood_group,location)

    subject = "Your Blood Donation Certificate"
    body = f"""
    Dear {donor_name},

    Thank you for your generous blood donation! Your contribution has made a meaningful difference,
    and we deeply appreciate your support.

    Please find your donation certificate attached as a token of our gratitude. 
    We hope it serves as a reminder of the lives you've helped.

    With warm regards,
    Youth Red Cross Team

    Contact us
    Phone: 9876543210
    Email: yrclifebloodsupport@gmail.com
    """

    send_email(subject, donor_email, body, certificate_path)

    return "Success"

@manage_donors.route('/reply_user_query',methods = ['POST','GET'])
def reply_user_query():
    if request.method == 'POST':
        query_id = request.form.get('query_id')
        admin_response = request.form.get('admin_response')
        admin_id = session.get('admin_id')
        admin_name = session.get('admin_name')
        
        # Fetch the query and update
        query = QueryTable.query.filter_by(id=query_id).first()
        if query:
            query.admin_response = admin_response
            query.admin_response_date = date.today()
            query.admin_id = admin_id
            query.admin_name = admin_name
            db.session.commit()
            flash("Response submitted successfully!", "success")
        else:
            flash("Query not found.", "error")
        return redirect(url_for('admin.render_query_page_admin_side'))
    
    # Render admin query page
    queries = QueryTable.query.all()
    return render_template('admin_query.html', queries=queries)