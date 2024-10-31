from flask import render_template , Blueprint , request
from app.utils.data_manipulations_toDB import FetchDetails

closing_requests = Blueprint('close_request',__name__)

@closing_requests.route('/close_expired_requests',methods = ['POST','GET'])
def close_expired_requests():
    if request.method == 'POST':
        request_id = request.form.get('request_id')
        response_status = request.form.get('response_status')
        report = request.form.get('report')
        units_donated = request.form.get('units_donated')
        response_donor_ids = request.form.get('response_donor_ids')

        FetchDetails.update_expired_request(
            request_id=request_id,
            response_status=response_status,
            report=report,
            units_donated=units_donated,
            response_donor_ids=response_donor_ids
        )
        
        return render_template('expired_requests_updation_confirmation.html')
    return render_template('index.html')

@closing_requests.route('/close_ongoing_requests',methods = ['POST','GET'])
def close_ongoing_requests():
    if request.method == 'POST':
        request_id = request.form.get('request_id')
        response_status = request.form.get('response_status')
        report = request.form.get('report')
        units_donated = request.form.get('units_donated')
        response_donor_ids = request.form.get('response_donor_ids')

        FetchDetails.update_ongoing_request(
            request_id=request_id,
            response_status=response_status,
            report=report,
            units_donated=units_donated,
            response_donor_ids=response_donor_ids
        )
        
        return render_template('expired_requests_updation_confirmation.html')
    return render_template('index.html')