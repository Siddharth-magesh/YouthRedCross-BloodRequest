from flask import Blueprint, request, jsonify
from app.utils.distance_analysis import DistanceConfiguration
from app.config import Config

fetch_availabe_donors = Blueprint('fetch_donors', __name__)
val = Config()

distance_calculator = DistanceConfiguration(
    api_key=val.GOOGLE_MAPS_API,
    base_url=val.BASE_MAPS_URL
)

@fetch_availabe_donors.route('/get_donors', methods=['POST'])
def get_donors():
    try:
        # Parse incoming JSON data
        data = request.get_json()
        blood_group = data.get('bloodType')
        hospital_address = data.get('hospitalAddress')

        if not blood_group:
            return jsonify({"error": "Blood group is required"}), 400
        
        unsorted_data = distance_calculator.fetch_matched_data(blood_group)

        if not unsorted_data or unsorted_data[0].get("Name") is None:
            return jsonify([])

        if hospital_address:
            sorted_data = distance_calculator.sorted_array_min_distance(
                available_donars=unsorted_data,
                target_address=hospital_address
            )
            return jsonify(sorted_data) 
        else:
            for donor in unsorted_data:
                donor['distance'] = None
            return jsonify(unsorted_data) 
    except Exception as e:
        return jsonify({"error": str(e)}), 500
