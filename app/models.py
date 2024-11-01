from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DonorDetail(db.Model):
    __tablename__ = 'DonorDetail'
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100),unique = True,nullable=False)
    password = db.Column(db.String(500), nullable=False)
    blood_group = db.Column(db.String(10), nullable=False)
    personal_details_id = db.Column(db.String(36), db.ForeignKey('PersonalDetailsUser.id'), nullable=False)
    address_id = db.Column(db.String(36), db.ForeignKey('AddressDetailsUser.id'), nullable=False)
    active_status = db.Column(db.Boolean, nullable=False, default=True)
    disease_id = db.Column(db.String(36), db.ForeignKey('DiseaseDetailsUser.id'))
    authentication_id = db.Column(db.String(36),unique=True, nullable=False)
    last_donated_date = db.Column(db.DateTime, nullable=True) 
    number_of_times_donated = db.Column(db.String(36),nullable=False)
    last_login_date = db.Column(db.DateTime, nullable=True)

class AuthenticationDetailsDonor(db.Model):
    __tablename__ = 'AuthenticationDetailsDonor'
    id = db.Column(db.Integer,primary_key=True)
    auth_id = db.Column(db.String(36),nullable=False)  
    name = db.Column(db.String(100), nullable=False)
    login_date = db.Column(db.Date, nullable=True)
    login_time = db.Column(db.Time, nullable=True)

class PersonalDetailsUser(db.Model):
    __tablename__ = 'PersonalDetailsUser'
    id = db.Column(db.String(36), primary_key=True)  
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=True)
    age = db.Column(db.Integer, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    secondary_contact_number = db.Column(db.String(15), nullable=True)
    marital_status = db.Column(db.String(10), nullable=True)
    aadhar_number = db.Column(db.String(20), nullable=True)

class AddressDetailsUser(db.Model):
    __tablename__ = 'AddressDetailsUser'
    id = db.Column(db.String(36), primary_key=True) 
    address = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(45), nullable=False)
    state = db.Column(db.String(45), nullable=False)
    city = db.Column(db.String(45), nullable=False)

class DiseaseDetailsUser(db.Model):
    __tablename__ = 'DiseaseDetailsUser'
    id = db.Column(db.String(36), primary_key=True)  
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)

class AdminDetails(db.Model):
    __tablename__ = 'AdminDetails'
    id = db.Column(db.String(36), primary_key=True) 
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    username = db.Column(db.String(45), nullable=False)
    authentication_id = db.Column(db.String(36),unique=True, nullable=False)
    vec_registration_number = db.Column(db.String(36),unique=True,nullable=False)
    data_of_birth = db.Column(db.Date,nullable=False)
    mobile_number = db.Column(db.String(36),nullable=False)
    department = db.Column(db.String(50),nullable=True)
    active_status = db.Column(db.String(36),nullable=False)
    last_login_date = db.Column(db.DateTime, nullable=True)
    approved_donation = db.Column(db.String(36), nullable=True) #Need To handle This value using Session
    closed_requests = db.Column(db.String(36), nullable=True)#Need To handle This value using Sessions

class AuthenticationDetailsAdmin(db.Model):
    __tablename__ = 'AuthenticationDetailsAdmin'
    id = db.Column(db.Integer,primary_key=True)
    auth_id = db.Column(db.String(36),nullable=False) 
    name = db.Column(db.String(100), nullable=False)
    login_date = db.Column(db.Date, nullable=False)
    login_time = db.Column(db.Time, nullable=False)

class BloodRequestDetails(db.Model):
    __tablename__ = 'BloodRequestDetails'
    id = db.Column(db.String(36), primary_key=True)  
    patient_name = db.Column(db.String(100), nullable=False)
    blood_group = db.Column(db.String(10), nullable=False)
    hospital_name = db.Column(db.String(100), nullable=False)
    hospital_id = db.Column(db.String(36), db.ForeignKey('HospitalDetails.id'), nullable=False)  
    contact_number = db.Column(db.String(15), nullable=False)
    patient_age = db.Column(db.Integer, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    request_reason = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(45), nullable=False)
    units_required = db.Column(db.Integer, nullable=False)
    attendant_name = db.Column(db.String(100), nullable=True)
    response_id = db.Column(db.String(36), db.ForeignKey('ResponseDetails.id') , nullable=False)
    approved_admin_id = db.Column(db.String(36), nullable=True) #Need To handle This value using Session
    closed_admin_id = db.Column(db.String(36), nullable=True) #Need To handle This value using Session

class HospitalDetails(db.Model):
    __tablename__ = 'HospitalDetails'
    id = db.Column(db.String(36), primary_key=True)  
    hospital_name = db.Column(db.String(100), nullable=False)
    hospital_address = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(45), nullable=False)
    state = db.Column(db.String(45), nullable=False)
    country = db.Column(db.String(45), nullable=False)
    branch = db.Column(db.String(45), nullable=True)
    landmark = db.Column(db.String(100), nullable=True)

class ResponseDetails(db.Model):
    __tablename__ = 'ResponseDetails'
    id = db.Column(db.String(36), primary_key=True)  
    status = db.Column(db.String(45), nullable=True)
    report = db.Column(db.String(255), nullable=True)
    units_donated = db.Column(db.Integer, nullable=True)
    donor_ids = db.Column(db.String(255), nullable=True) 
