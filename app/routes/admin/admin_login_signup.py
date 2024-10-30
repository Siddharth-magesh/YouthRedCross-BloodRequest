from flask import Blueprint, render_template , request , redirect , url_for
from app.database import AdminDetails
from werkzeug.security import check_password_hash

admin_authentications = Blueprint('admin_auth',__name__)

@admin_authentications.route('/validate_admin',methods=['POST','GET'])
def validate_admin():
    email = request.form.get('email')
    password = request.form.get('password')

    admin = AdminDetails.query.filter_by(email=email).first()
    #if admin and check_password_hash(admin.password, password): #Check using Hashed Password
    if admin.password == password:
        return redirect(url_for('admin.render_main_admin_page'))
    else:
        return "Invalid email or password", 401
    
@admin_authentications.route('/Signup_New_Admin',methods=['POST','GET'])
def Signup_New_Admin():
    return "SignUp Page"