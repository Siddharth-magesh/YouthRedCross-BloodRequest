import smtplib
from email.mime.text import MIMEText
from app.config import Config
from app.models import db , DonorDetail

cred = Config()

def send_email(subject, recipient, body):
    msg = MIMEText(body,"html")
    msg['Subject'] = subject
    msg['From'] = cred.BASE_MAIL_ADDRESS
    msg['To'] = recipient

    with smtplib.SMTP(cred.MAIL_SERVER, cred.MAIL_PORT) as server:
        server.starttls() 
        server.login(cred.MAIL_USERNAME, cred.MAIL_PASSWORD)
        server.sendmail(cred.BASE_MAIL_ADDRESS, recipient, msg.as_string())

def Welcome_message():
    subject = "Welcome to LifeConnect – Your Journey Begins Here"
    donors = db.session.query(
        DonorDetail.name,
        DonorDetail.email
    ).all()

    for donor in donors:
        name = donor.name
        email = donor.email

        body = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; background-color: #f9f9f9; margin: 0; padding: 0;">
            <div style="background-color: #ffffff; margin: 20px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; max-width: 600px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                <div style="background-color: #8B0000; color: white; padding: 15px; text-align: center; border-radius: 8px 8px 0 0; font-size: 20px; font-weight: bold;">
                    Welcome to LifeConnect
                </div>
                <div style="padding: 20px; font-size: 16px; color: #333;">
                    <p>Dear {name},</p>
                    
                    <p style="font-size: 16px; color: #333;">
                        Thank you for joining <strong>LifeConnect</strong>. We are thrilled to have you as part of our blood donation community. Your selfless contribution has the potential to save lives and inspire others to do the same.
                    </p>
                    
                    <p style="font-size: 16px; color: #333;">
                        To learn more about us and explore our platform, click the link below:
                    </p>
                    <p style="text-align: center; margin: 20px 0;">
                        <a href="https://www.lifeconnect.org" style="font-size: 16px; color: #ffffff; background-color: #8B0000; padding: 10px 20px; border-radius: 4px; text-decoration: none;">
                            Visit LifeConnect
                        </a>
                    </p>

                    <p style="font-size: 16px; color: #333;">
                        Share this opportunity with your friends and family who may also be interested in making a difference. Together, we can build a stronger, healthier community.
                    </p>

                    <p style="font-size: 16px; color: #333;">
                        If you have any questions or need assistance, feel free to contact us at <a href="mailto:yrclifeconnect@gmail.com" style="color: #8B0000; text-decoration: none;">yrclifeconnect@gmail.com</a>.
                    </p>
                    
                    <hr style="border: 0; height: 1px; background-color: #ddd; margin: 20px 0;">

                    <p style="margin-top: 20px; text-align: center; font-size: 14px; color: #555;">
                        © LifeConnect. All rights reserved.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        try:
            send_email(subject, email, body)
            print(f"Welcome email sent successfully to {name} ({email}).")
        except Exception as e:
            print(f"Failed to send email to {name} ({email}): {e}")
