from flask import Blueprint, render_template , request
from app.database import AdminDetails

admin_authentications = Blueprint('admin_auth',__name__)

@admin_authentications.route('/validate_admin',methods=['POST','GET'])
def validate_admin():
    email = request.form.get('email')
    password = request.form.get('password')

    admin = AdminDetails.query.filter_by(email=email).first()
    if admin.password == password:
        return "Success"
    else:
        return "Invalid email or password", 401
    