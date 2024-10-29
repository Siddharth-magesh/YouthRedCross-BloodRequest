from flask import Blueprint , render_template , request

generate_blood_request = Blueprint('generate_blood_request',__name__)

@generate_blood_request.route('/generate_bloodRequest',methods=['POST','GET'])
def generate_bloodRequest():
    return render_template('index.html')