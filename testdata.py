from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import random

# Set up the database connection and session
DATABASE_URL = "mysql+mysqlconnector://root:ocalhost/YouthRedCross_BloodRequest"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Sample data insertion script
def insert_synthetic_data():
    try:
        # Insert into PersonalDetailsUser table
        for i in range(1, 11):
            first_name = f"FirstName_{i}"
            last_name = f"LastName_{i}"
            age = random.randint(18, 65)
            dob = datetime.now() - timedelta(days=age * 365)
            contact_number = f"123456789{i}"
            secondary_contact_number = f"987654321{i}" if i % 2 == 0 else None
            marital_status = random.choice([0, 1])
            aadhar_number = f"1234 5678 90{i}"

            session.execute(
                "INSERT INTO PersonalDetailsUser (FirstName, LastName, Age, DateOfBirth, ContactNumber, SecondaryContactNumber, MatrialStatus, AadharNumber) "
                "VALUES (:first_name, :last_name, :age, :dob, :contact_number, :secondary_contact_number, :marital_status, :aadhar_number)",
                {
                    'first_name': first_name,
                    'last_name': last_name,
                    'age': age,
                    'dob': dob,
                    'contact_number': contact_number,
                    'secondary_contact_number': secondary_contact_number,
                    'marital_status': marital_status,
                    'aadhar_number': aadhar_number
                }
            )

        # Insert into AddressDetailsUser table
        for i in range(1, 11):
            address = f"Street {i}, Area {i}"
            pincode = 600000 + i
            country = "India"
            state = "State_" + str(i)
            city = "City_" + str(i)

            session.execute(
                "INSERT INTO AddressDetailsUser (Address, Pincode, Country, State, City) "
                "VALUES (:address, :pincode, :country, :state, :city)",
                {
                    'address': address,
                    'pincode': pincode,
                    'country': country,
                    'state': state,
                    'city': city
                }
            )

        # Commit all insertions
        session.commit()
        print("Synthetic data inserted successfully.")
        
    except Exception as e:
        session.rollback()
        print(f"Error inserting data: {e}")
    finally:
        session.close()

# Run the synthetic data insertion
if __name__ == "__main__":
    insert_synthetic_data()
