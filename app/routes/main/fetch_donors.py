# app/routes/find_donor.py
from flask import Blueprint, render_template, request
from app.utils.distance_analysis import DistanceConfiguration
from app.config import Config

fetch_availabe_donors = Blueprint('fetch_donors', __name__)
val = Config()

distance_calculator = DistanceConfiguration(
    api_key=val.GOOGLE_MAPS_API,
    base_url=val.BASE_MAPS_URL
)

@fetch_availabe_donors.route('/get_donors', methods=['GET', 'POST'])
def get_donors():
    if request.method == 'POST':
        blood_group = request.form.get('bloodType')
        hospital_address = request.form.get('hospital_address')  # Assuming you'll add this input later

        # Fetch matched donors based on blood group
        unsorted_data = distance_calculator.fetch_matched_data(blood_group)
        
        if hospital_address:
            # If a hospital address is provided, sort the donors by proximity
            sorted_data = distance_calculator.sorted_array_min_distance(
                available_donars=unsorted_data,
                target_address=hospital_address
            )
            return render_template('fetch_donors.html', donors=sorted_data)
        else:
            # If no hospital address is provided, return donors without distance
            for donor in unsorted_data:
                donor['distance'] = None  # Set distance to None if no address is provided
            return render_template('fetch_donors.html', donors=unsorted_data)
    
    # Render the page without donor data for GET request
    return render_template('fetch_donors.html', donors=[])

