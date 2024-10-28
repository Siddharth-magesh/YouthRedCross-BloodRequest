# app/routes/find_donor.py
from flask import Blueprint, render_template, request

fetch_availabe_donors = Blueprint('fetch_donors', __name__)

@fetch_availabe_donors.route('/get_donors', methods=['GET', 'POST'])
def get_donors():
    if request.method == 'POST':
        blood_type = request.form.get('bloodType')

        donors = [
            {
                "Name": "John Doe",
                "blood_grp": "A+",
                "city": "New York",
                "address": "123 Elm Street",
                "status": "Active",
                "distance": 5.3
            },
            {
                "Name": "Jane Smith",
                "blood_grp": "B+",
                "city": "Los Angeles",
                "address": "456 Oak Avenue",
                "status": "Active",
                "distance": 12.1
            }
        ]

        filtered_donors = [donor for donor in donors if donor['blood_grp'] == blood_type]
        return render_template('fetch_donors.html', donors=filtered_donors)
    
    # Render the page without donor data for GET request
    return render_template('fetch_donors.html', donors=[])
