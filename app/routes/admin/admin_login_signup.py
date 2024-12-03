from flask import Blueprint, render_template , request , redirect , url_for , flash , session , current_app
from app.models import AdminDetails , AuthenticationDetailsAdmin , db
from werkzeug.security import check_password_hash , generate_password_hash
from datetime import datetime
import secrets
import smtplib
from email.mime.text import MIMEText
from app.config import Config

cred = Config()
admin_authentications = Blueprint('admin_auth',__name__)

def generate_secure_numeric_otp(length=6):
    otp = ''.join(str(secrets.randbelow(10)) for _ in range(length))
    return otp

def send_email(subject, recipient, body):
    msg = MIMEText(body,"html")
    msg['Subject'] = subject
    msg['From'] = cred.BASE_MAIL_ADDRESS
    msg['To'] = recipient

    with smtplib.SMTP(cred.MAIL_SERVER, cred.MAIL_PORT) as server:
        server.starttls() 
        server.login(cred.MAIL_USERNAME, cred.MAIL_PASSWORD)
        server.sendmail(cred.BASE_MAIL_ADDRESS, recipient, msg.as_string())

def get_next_id(table,prefix):
    max_id = db.session.query(table.id).order_by(table.id.desc()).first()
    next_id_num = 1
    if max_id:
        current_num = int(max_id[0][len(prefix):])
        next_id_num = current_num + 1
    return f"{prefix}{str(next_id_num).zfill(3)}"

def get_next_id_secondary(table,prefix):
    max_id = db.session.query(table.authentication_id).order_by(table.authentication_id.desc()).first()
    next_id_num = 1
    if max_id:
        current_num = int(max_id[0][len(prefix):])
        next_id_num = current_num + 1
    return f"{prefix}{str(next_id_num).zfill(3)}"

@admin_authentications.route('/validate_admin',methods=['POST','GET'])
def validate_admin():
    email = request.form.get('email')
    password = request.form.get('password')
    captcha = current_app.extensions.get('captcha')

    if not captcha or not captcha.validate():
        flash("Invalid CAPTCHA. Please try again.", "error")
        return redirect(url_for('admin.render_admin_login'))

    admin = AdminDetails.query.filter_by(email=email).first()

    if admin and check_password_hash(admin.password, password):
        current_datetime = datetime.now()
        current_date = current_datetime.date()
        current_time = current_datetime.time()
        admin.last_login_date = current_datetime

        session['admin_id'] = admin.id
        session['logged_in'] = True
        session['admin_name'] = admin.username
        session.permanent = True

        logging_details = AuthenticationDetailsAdmin(
            auth_id = admin.authentication_id,
            name = admin.username,
            login_date = current_date,
            login_time = current_time
        )
        db.session.add(logging_details)
        db.session.commit()
        return redirect(url_for('admin.render_main_admin_page'))
    else:
        return "Invalid email or password", 401
    
@admin_authentications.route('/register_new_admin',methods=['POST','GET'])
def register_new_admin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        username = request.form.get('username')
        vec_registration_number = request.form.get('vec_registration_number')
        date_of_birth = request.form.get('date_of_birth')
        mobile_number = request.form.get('mobile_number')
        department = request.form.get('department')
        admin_id = get_next_id(AdminDetails, 'ADMIN')
        authentication_id = get_next_id_secondary(AdminDetails,'AUTHADM')


        if password != confirm_password:
            flash('Make sure you enter similar passwords', 'danger')
            return render_template('register_donor.html')
        
        one_time_password = generate_secure_numeric_otp()

        active_admins = AdminDetails.query.filter_by(active_status='Active').all()
        active_admin_emails = [admin.email for admin in active_admins]
        for admin_email in active_admin_emails:
            subject = "New Admin Registration Request"
            recipient = admin_email
            body = f"""
            <!DOCTYPE html>
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; background-color: #f9f9f9; margin: 0; padding: 0;">
                <div style="background-color: #ffffff; margin: 20px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; max-width: 600px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                    <div style="background-color: #8B0000; color: white; padding: 15px; text-align: center; border-radius: 8px 8px 0 0; font-size: 20px; font-weight: bold;">
                        New Admin Sign-Up Verification
                    </div>
                    <div style="padding: 20px; font-size: 16px; color: #333;">
                        <p>Dear Admin,</p>
                        
                        <p style="font-size: 16px; color: #333;">
                            A new admin sign-up has been generated. Kindly verify the admin details and share the OTP only if the information is valid.
                        </p>
                        
                        <p style="font-size: 16px; color: #333;">
                            <strong style="color: #8B0000;">New Admin Details:</strong>
                        </p>
                        <ul style="font-size: 16px; color: #333;">
                            <li><strong>Email:</strong> {email}</li>
                            <li><strong>Name:</strong> {username}</li>
                            <li><strong>VEC Registration Number:</strong> {vec_registration_number}</li>
                            <li><strong>Date of Birth:</strong> {date_of_birth}</li>
                            <li><strong>Mobile Number:</strong> {mobile_number}</li>
                            <li><strong>Department:</strong> {department}</li>
                            <li><strong>Generated Admin ID:</strong> {admin_id}</li>
                            <li><strong>Generated Authentication ID:</strong> {authentication_id}</li>
                        </ul>
                        
                        <p style="font-size: 16px; color: #333;">
                            Please share the below credentials with the new admin for further verification:
                        </p>
                        <p style="font-size: 18px; font-weight: bold; color: #8B0000;">
                            {one_time_password}
                        </p>

                        <p style="margin-top: 20px; text-align: center; font-size: 14px; color: #555;">
                            Regards,<br>
                            <strong>Youth Red Cross Blood Donation Site</strong>
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """

            send_email(subject, recipient, body)

        return render_template(
            'admin_otp_verification_page.html',
            one_time_password=one_time_password,
            email=email,
            password=password,
            username=username,
            vec_registration_number=vec_registration_number,
            date_of_birth=date_of_birth,
            mobile_number=mobile_number,
            department=department,
            admin_id=admin_id,
            authentication_id=authentication_id
        )
    
@admin_authentications.route('/verify_otp_and_data_injection',methods=['POST','GET'])
def verify_otp_and_data_injection():
    entered_otp = request.form.get('otp')
    generated_otp = request.form.get('generated_otp')
    email = request.form.get('email')
    password = request.form.get('password')
    username = request.form.get('username')
    vec_registration_number = request.form.get('vec_registration_number')
    date_of_birth = request.form.get('date_of_birth')
    mobile_number = request.form.get('mobile_number')
    department = request.form.get('department')
    admin_id = request.form.get('admin_id')
    authentication_id = request.form.get('authentication_id')
    active_status = 'Active'
    last_login_date = None
    approved_donation = 0
    closed_donations = 0

    if entered_otp == generated_otp:
        hashed_password = generate_password_hash(password)
        new_admin = AdminDetails(
            id = admin_id,
            email = email,
            password = hashed_password,
            username = username,
            authentication_id = authentication_id,
            vec_registration_number = vec_registration_number,
            data_of_birth = date_of_birth,
            mobile_number = mobile_number,
            department = department,
            active_status = active_status,
            last_login_date = last_login_date,
            approved_donation_count = approved_donation,
            closed_requests_count = closed_donations
        )
        db.session.add(new_admin)
        db.session.commit()
        
        flash('Admin account created successfully.', 'success')
        return redirect(url_for('admin.render_admin_login'))
    else:
        flash('Invalid Otp')

@admin_authentications.route('/manage_forget_password_admin',methods=['POST','GET'])
def manage_forget_password_admin():
    email = request.form.get('email')
    one_time_password = generate_secure_numeric_otp()

    fetched_donor = AdminDetails.query.filter_by(email=email).first()

    if fetched_donor and fetched_donor.email == email:
        subject = "Request for Password Change"
        recipient = email
        link = "http://127.0.0.1:5000/main/render_query_page"
        body = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; background-color: #f9f9f9; margin: 0; padding: 0;">
            <div style="background-color: #ffffff; margin: 20px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; max-width: 600px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                <div style="background-color: #8B0000; color: white; padding: 15px; text-align: center; border-radius: 8px 8px 0 0; font-size: 20px; font-weight: bold;">
                    Password Change Request Verification
                </div>
                <div style="padding: 20px; font-size: 16px; color: #333;">
                    <p>Dear Admin,</p>
                    
                    <p style="font-size: 16px; color: #333;">
                        We have received a request from your YRC-LBS account to change your password. If you did not initiate this request, please let us know by clicking the link below:
                    </p>
                    
                    <p style="text-align: center;">
                        <a href="{link}" style="font-size: 16px; text-decoration: none; color: white; background-color: #007bff; padding: 10px 20px; border-radius: 5px;">
                            Report Issue
                        </a>
                    </p>
                    
                    <p style="font-size: 16px; color: #333;">
                        If you did request the password change, please use the following OTP to proceed with updating your password:
                    </p>
                    
                    <p style="font-size: 18px; font-weight: bold; color: #8B0000; text-align: center;">
                        {one_time_password}
                    </p>

                    <p style="font-size: 16px; color: #333;">
                        Please note: Do not share this OTP with any third parties to ensure the security of your account.
                    </p>

                    <p style="margin-top: 20px; text-align: center; font-size: 14px; color: #555;">
                        Regards,<br>
                        <strong>Youth Red Cross Blood Donation Site</strong>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        send_email(subject, recipient, body)

        return render_template('otp_validation_admin.html',one_time_password=one_time_password,email=email)
    else:
        flash("An error occurred:")
        return "An error occurred while updating the donor details", 500
    
@admin_authentications.route('/otp_validation_admin',methods=['POST','GET'])
def otp_validation_admin():
    generate_otp = request.form.get('generated_otp')
    typed_otp = request.form.get('typed_otp')
    email = request.form.get('email')
    print("here also")

    if str(generate_otp) == str(typed_otp):
        return render_template('admin_new_password.html',email=email)
    else :
        return "Wrong One Time Password"
    
@admin_authentications.route('/new_password_admin',methods=['POST','GET'])
def new_password_admin():
    password = request.form.get('password')
    confirmpassword = request.form.get('confirmpassword')
    email = request.form.get('email')

    if password==confirmpassword:
        donor = AdminDetails.query.filter_by(email=email).first()
        hashed_password = generate_password_hash(password)
        donor.password = hashed_password
        db.session.commit()
        print("here")
        return redirect(url_for('admin.render_admin_login'))
    else:
        return "Couldnt Update the password"
    

@admin_authentications.route('/update_admin_details',methods=['POST','GET'])
def update_admin_details():
    admin_id = request.form.get('id')
    name = request.form.get('name')
    email = request.form.get('email')
    vec_registration_number = request.form.get('vec_registration_number')
    active_status = request.form.get('active_status')
    department = request.form.get('department')
    approved_donation_count = request.form.get('approved_donation')
    closed_requests_count = request.form.get('closed_requests')
    contact_number = request.form.get('contact_number')
    date_of_birth = request.form.get('date_of_birth')

    admin_details = AdminDetails.query.get(admin_id)
    if name and name != admin_details.id:
        admin_details.username = name
    if email and email != admin_details.email:
        admin_details.email = email
    if vec_registration_number and vec_registration_number != admin_details.vec_registration_number:
        admin_details.vec_registration_number = vec_registration_number
    if active_status and active_status != admin_details.active_status:
        admin_details.active_status = active_status
    if department and department != admin_details.department:
        admin_details.department = department
    if approved_donation_count and approved_donation_count != admin_details.approved_donation_count:
        admin_details.approved_donation_count = approved_donation_count
    if closed_requests_count and closed_requests_count != admin_details.closed_requests_count:
        admin_details.closed_requests_count = closed_requests_count
    if contact_number and contact_number != admin_details.mobile_number:
        admin_details.mobile_number = contact_number
    if date_of_birth and date_of_birth != admin_details.date_of_birth:
        admin_details.date_of_birth = date_of_birth
    
    try:
        db.session.commit()
        flash("Donor details updated successfully.")
        return redirect(url_for('admin.render_main_admin_page'))
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {e}")
        return "An error occurred while updating the donor details", 500
