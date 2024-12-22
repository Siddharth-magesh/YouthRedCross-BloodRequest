import requests
import re
from app.models import PersonalDetailsUser , DonorDetail , AddressDetailsUser , db

class DistanceConfiguration:
    def __init__(self, api_key, base_url, ) -> None:
        """
        Initialize the DistanceConfiguration object with API key, base URL, and MySQL database credentials.
        """
        self.api_key = api_key
        self.base_url = base_url

    def get_distance(self, start_location, end_location):
        """
        Calculate the distance between two locations using the Google Maps Distance Matrix API.

        :param start_location: Origin address.
        :param end_location: Destination address.
        :return: Distance as a float in kilometers (or other unit), or float('inf') on failure.
        """
        params = {
            "origins": start_location,
            "destinations": end_location,
            "key": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data['status'] == "OK" and data['rows']:
                distance_text = data['rows'][0]['elements'][0]['distance']['text']
                distance_value = float(re.findall(r"[\d\.]+", distance_text)[0])
                return distance_value
            else:
                print('Request Failed')
                return float('inf') 
        else:
            print("Failed to make Request")
            return float('inf')

    def fetch_matched_data(self, blood_group_provided):
        """
        Fetch active donor data from the MySQL database based on the provided blood group.

        :param blood_group: The blood group to filter donors.
        :return: A list of dictionaries containing donor information, or None on failure.
        [
            {
                "Name": "John Doe",
                "blood_grp": "A+",
                "city": "New York",
                "address": "123 Elm Street",
                "status": "Active"
            },
            {
                "Name": "Robert",
                "blood_grp": "A+",
                "city": "New York",
                "address": "123 Lombard Street",
                "status": "Active"
            }
        ]
        """
        try:
            results = (
                db.session.query(
                    PersonalDetailsUser.first_name.label("Name"),
                    DonorDetail.blood_group.label("blood_grp"),
                    AddressDetailsUser.city,
                    AddressDetailsUser.address,
                    DonorDetail.active_status.label("status")
                )
                .join(PersonalDetailsUser, DonorDetail.personal_details_id == PersonalDetailsUser.id)
                .join(AddressDetailsUser, DonorDetail.address_id == AddressDetailsUser.id)
                .filter(DonorDetail.blood_group == blood_group_provided, DonorDetail.active_status == True)
                .all()
            )

            if not results:
                return [{"Name": None, "blood_grp": None, "city": None, "address": None, "status": None}]

            result_list = [
                {
                    "Name": row.Name,
                    "blood_grp": row.blood_grp,
                    "city": row.city,
                    "address": row.address,
                    "status": "Active" if row.status else "Inactive"
                }
                for row in results
            ]
            return result_list if result_list else None

        except Exception as e:
            print(f"Error Fetching Data: {e}")
            return None

        
    def sorted_array_min_distance(self, available_donars, target_address):
        """
        Sort the list of donors based on the distance from a target address.

        :param available_donars: A list of donors with details fetched from the database.
        :param target_address: The target address to calculate distances from.
        :return: A list of donors sorted by proximity to the target address.
        [
            {
                "Name": "John Doe",
                "blood_grp": "A+",
                "city": "New York",
                "address": "123 Elm Street",
                "status": "Active",
                "distance": 5.3  # Distance from target_address
            },
            {
                "Name": "Jane Smith",
                "blood_grp": "B+",
                "city": "Los Angeles",
                "address": "456 Oak Avenue",
                "status": "Active",
                "distance": 12.1  # Distance from target_address
            }
        ]
        """
        for donar in available_donars:
            distance = self.get_distance(
                start_location=target_address,
                end_location=donar['address']
            )
            donar['distance'] = distance

        donars_sorted = sorted(available_donars, key=lambda x: x['distance'])
        return donars_sorted