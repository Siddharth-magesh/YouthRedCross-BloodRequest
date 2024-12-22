from flask import Blueprint, request, jsonify , redirect ,  flash , render_template, url_for
from datetime import date
from app.utils.distance_analysis import DistanceConfiguration
from app.config import Config
from app.models import QueryTable , db

fetch_availabe_donors = Blueprint('fetch_donors', __name__)
val = Config()

distance_calculator = DistanceConfiguration(
    api_key=val.GOOGLE_MAPS_API,
    base_url=val.BASE_MAPS_URL
)

@fetch_availabe_donors.route('/get_donors', methods=['POST'])
def get_donors():
    try:
        blood_group = request.form.get('bloodType')
        hospital_address = request.form.get('hospital_address')

        if not blood_group:
            return jsonify({"error": "Blood group is required"}), 400
        
        unsorted_data = distance_calculator.fetch_matched_data(blood_group)

        if not unsorted_data or unsorted_data[0].get("Name") is None:
            return render_template('available_donors.html',data=[]) 

        if hospital_address:
            sorted_data = distance_calculator.sorted_array_min_distance(
                available_donars=unsorted_data,
                target_address=hospital_address
            )
            return render_template('available_donors.html',data=sorted_data) 
        else:
            for donor in unsorted_data:
                donor['distance'] = None
            return render_template('available_donors.html',data=unsorted_data) 
    except Exception as e:
        return "Error in Fetching the Donors"

@fetch_availabe_donors.route('/get_user_query', methods=['POST', 'GET'])
def get_user_query():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        user_email = request.form.get('user_email')
        user_query = request.form.get('user_query')
        
        if user_name and user_email and user_query:
            new_query = QueryTable(
                user_name=user_name,
                user_email=user_email,
                user_query=user_query,
                user_query_date=date.today(),
                admin_id="PENDING",
                admin_name="PENDING"
            )
            db.session.add(new_query)
            db.session.commit()
            flash("Your query has been submitted successfully!", "success")
        else:
            flash("Please fill in all fields.", "error")
        return redirect(url_for('main.render_query_page'))
        
    queries = QueryTable.query.all()
    return render_template('render_query_page.html', queries=queries)