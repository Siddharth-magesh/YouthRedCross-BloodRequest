from app.models import BloodRequestDetails, HospitalDetails, DonorDetail, ResponseDetails, PersonalDetailsUser , AddressDetailsUser, DiseaseDetailsUser,AdminDetails,db
from sqlalchemy import func
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from datetime import datetime , timedelta
from flask import session
import json

class FetchDetails:
    @staticmethod
    def get_new_requests():
        new_requests = (
            db.session.query(
                BloodRequestDetails.id.label("request_id"),
                BloodRequestDetails.patient_name,
                BloodRequestDetails.patient_age,
                BloodRequestDetails.blood_group,
                BloodRequestDetails.units_required,
                HospitalDetails.hospital_name.label("hospital_name"),
                HospitalDetails.hospital_address.label("hospital_address"),
                HospitalDetails.id.label("hospital_id"),
                BloodRequestDetails.status,
                BloodRequestDetails.due_date,
                BloodRequestDetails.contact_number,
                BloodRequestDetails.attendant_name,
                BloodRequestDetails.request_reason,
                db.session.query(db.func.count(DonorDetail.id))
                .filter(
                    DonorDetail.blood_group == BloodRequestDetails.blood_group,
                    DonorDetail.active_status == True
                ).label("active_donor_count")
            )
            .join(HospitalDetails, BloodRequestDetails.hospital_id == HospitalDetails.id)
            .filter(BloodRequestDetails.status == "Not_Approved")
            .all()
        )
        return new_requests

    @staticmethod
    def update_the_new_requests(request_id):
        try:
            request_to_update = db.session.query(BloodRequestDetails).filter(BloodRequestDetails.id == request_id).first()
            if request_to_update:
                request_to_update.status = "Pending"
                request_to_update.approved_admin_id = session.get('admin_id')
                db.session.commit()
                admin_details = AdminDetails.query.filter_by(id = session.get('admin_id')).first()
                admin_details.approved_donation_count = admin_details.approved_donation_count + 1
                response_to_update = db.session.query(ResponseDetails).filter(ResponseDetails.id == request_to_update.response_id).first()
                if response_to_update:
                    response_to_update.status = "Pending"
                    db.session.commit()
                else:
                    print(f"No response found for request {request_id}.")
            else:
                print(f"Request {request_id} not found.")
        except Exception as e:
            db.session.rollback()
            print(f"Error updating request {request_id}: {e}")

    @staticmethod
    def Decline_new_requests(request_id):
        try:
            request_to_update = db.session.query(BloodRequestDetails).filter(BloodRequestDetails.id == request_id).first()
            
            if not request_to_update:
                print(f"Request {request_id} not found.")
                return False, f"Request {request_id} not found."
            
            request_to_update.status = "Closed"
            request_to_update.approved_admin_id = session.get('admin_id')
            request_to_update.closed_admin_id = session.get('admin_id')
            db.session.commit()

            admin_details = AdminDetails.query.filter_by(id = session.get('admin_id')).first()
            admin_details.approved_donation_count = admin_details.approved_donation_count + 1

            response_to_update = db.session.query(ResponseDetails).filter(ResponseDetails.id == request_to_update.response_id).first()
            
            if not response_to_update:
                print(f"No response found for request {request_id}.")
                return False, f"No response found for request {request_id}."
            
            response_to_update.status = "Declined"
            db.session.commit()
            
            return True, "Request and response successfully declined."
            
        except Exception as e:
            db.session.rollback()
            print(f"Error updating request {request_id}: {e}")
            return False, f"Error updating request {request_id}: {e}"


    @staticmethod
    def fetch_closed_requests():
        closed_results = (
            db.session.query(
                BloodRequestDetails.id,
                BloodRequestDetails.patient_name,
                BloodRequestDetails.blood_group,
                BloodRequestDetails.hospital_name,
                BloodRequestDetails.contact_number,
                BloodRequestDetails.patient_age,
                BloodRequestDetails.due_date,
                BloodRequestDetails.request_reason,
                BloodRequestDetails.status,
                BloodRequestDetails.units_required,
                BloodRequestDetails.attendant_name,
                BloodRequestDetails.response_id,
                BloodRequestDetails.approved_admin_id,
                BloodRequestDetails.closed_admin_id,
                ResponseDetails.status.label("response_status"),
                ResponseDetails.report,
                ResponseDetails.units_donated,
                ResponseDetails.certificate_status,
                ResponseDetails.donation_date,
                ResponseDetails.donor_ids.label("response_donor_ids"),
                HospitalDetails.hospital_address,
                HospitalDetails.id.label("hospital_id")
            )
            .join(ResponseDetails, BloodRequestDetails.response_id == ResponseDetails.id)
            .join(HospitalDetails, BloodRequestDetails.hospital_id == HospitalDetails.id)
            .filter(BloodRequestDetails.status == 'Closed')
            .all()
        )
        return closed_results
    
    @staticmethod
    def fetch_expired_requests():
        expired_results = (
            db.session.query(
                BloodRequestDetails.id,
                BloodRequestDetails.patient_name,
                BloodRequestDetails.blood_group,
                BloodRequestDetails.hospital_name,
                BloodRequestDetails.contact_number,
                BloodRequestDetails.patient_age,
                BloodRequestDetails.due_date,
                BloodRequestDetails.request_reason,
                BloodRequestDetails.status,
                BloodRequestDetails.units_required,
                BloodRequestDetails.attendant_name,
                BloodRequestDetails.response_id,
                BloodRequestDetails.approved_admin_id,
                BloodRequestDetails.closed_admin_id,
                ResponseDetails.status.label("response_status"),
                ResponseDetails.report,
                ResponseDetails.units_donated,
                ResponseDetails.certificate_status,
                ResponseDetails.donation_date,
                ResponseDetails.donor_ids.label("response_donor_ids"),
                HospitalDetails.hospital_address,
                HospitalDetails.id.label("hospital_id")
            )
            .join(ResponseDetails, BloodRequestDetails.response_id == ResponseDetails.id)
            .join(HospitalDetails, BloodRequestDetails.hospital_id == HospitalDetails.id)
            .filter(BloodRequestDetails.status == 'Expired')
            .all()
        )
        return expired_results
    
    @staticmethod
    def fetch_declined_requests():
        closed_results = (
            db.session.query(
                BloodRequestDetails.id,
                BloodRequestDetails.patient_name,
                BloodRequestDetails.blood_group,
                BloodRequestDetails.hospital_name,
                BloodRequestDetails.contact_number,
                BloodRequestDetails.patient_age,
                BloodRequestDetails.due_date,
                BloodRequestDetails.request_reason,
                BloodRequestDetails.status,
                BloodRequestDetails.units_required,
                BloodRequestDetails.attendant_name,
                BloodRequestDetails.response_id,
                BloodRequestDetails.approved_admin_id,
                BloodRequestDetails.closed_admin_id,
                ResponseDetails.status.label("response_status"),
                ResponseDetails.report,
                ResponseDetails.units_donated,
                ResponseDetails.certificate_status,
                ResponseDetails.donation_date,
                ResponseDetails.donor_ids.label("response_donor_ids"),
                HospitalDetails.hospital_address,
                HospitalDetails.id.label("hospital_id")
            )
            .join(ResponseDetails, BloodRequestDetails.response_id == ResponseDetails.id)
            .join(HospitalDetails, BloodRequestDetails.hospital_id == HospitalDetails.id)
            .filter(ResponseDetails.status == 'Declined')
            .all()
        )
        return closed_results

    @staticmethod
    def fetch_ongoing_requests():
        expired_results = (
            db.session.query(
                BloodRequestDetails.id,
                BloodRequestDetails.patient_name,
                BloodRequestDetails.blood_group,
                BloodRequestDetails.hospital_name,
                BloodRequestDetails.contact_number,
                BloodRequestDetails.patient_age,
                BloodRequestDetails.due_date,
                BloodRequestDetails.request_reason,
                BloodRequestDetails.status,
                BloodRequestDetails.units_required,
                BloodRequestDetails.attendant_name,
                BloodRequestDetails.response_id,
                BloodRequestDetails.approved_admin_id,
                BloodRequestDetails.closed_admin_id,
                ResponseDetails.status.label("response_status"),
                ResponseDetails.report,
                ResponseDetails.units_donated,
                ResponseDetails.certificate_status,
                ResponseDetails.donor_ids.label("response_donor_ids"),
                HospitalDetails.hospital_address,
                HospitalDetails.id.label("hospital_id")
            )
            .join(ResponseDetails, BloodRequestDetails.response_id == ResponseDetails.id)
            .join(HospitalDetails, BloodRequestDetails.hospital_id == HospitalDetails.id)
            .filter(BloodRequestDetails.status == 'Pending')
            .all()
        )
        return expired_results
    
    @staticmethod
    def update_expired_request(request_id,response_status,report,units_donated,certificate_status,donation_date,response_donor_ids):
        try:
            blood_request = BloodRequestDetails.query.filter_by(id=request_id).first()
            if not blood_request:
                raise ValueError("Blood request with the given ID does not exist.")

            blood_request.status = "Closed"
            blood_request.closed_admin_id = session.get('admin_id')

            admin_details = AdminDetails.query.filter_by(id=session.get('admin_id')).first()
            admin_details.closed_requests_count = admin_details.closed_requests_count + 1

            response_detail = ResponseDetails.query.filter_by(id=blood_request.response_id).first()
            if response_detail:
                response_detail.status = response_status
                response_detail.report = report
                response_detail.units_donated = units_donated
                response_detail.donor_ids = response_donor_ids
                response_detail.donation_date = donation_date
                response_detail.certificate_status = certificate_status
            else:
                raise ValueError("No response found for the given blood request.")

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")
            raise

    @staticmethod
    def update_ongoing_request(request_id,response_status,report,units_donated,certificate_status,donation_date,response_donor_ids):
        try:
            blood_request = BloodRequestDetails.query.filter_by(id=request_id).first()
            if not blood_request:
                raise ValueError("Blood request with the given ID does not exist.")

            blood_request.status = "Closed"
            blood_request.closed_admin_id = session.get('admin_id')

            admin_details = AdminDetails.query.filter_by(id=session.get('admin_id')).first()
            admin_details.closed_requests_count = admin_details.closed_requests_count + 1

            response_detail = ResponseDetails.query.filter_by(id=blood_request.response_id).first()
            if response_detail:
                response_detail.status = response_status
                response_detail.report = report
                response_detail.units_donated = units_donated
                response_detail.donor_ids = response_donor_ids
                response_detail.donation_date = donation_date
                response_detail.certificate_status = certificate_status
            else:
                raise ValueError("No response found for the given blood request.")

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")
            raise

    @staticmethod
    def fetch_donor_details(donor_id):
        try:
            donor_detail = (
                db.session.query(
                    DonorDetail.id,
                    DonorDetail.name,
                    DonorDetail.email,
                    DonorDetail.password,
                    DonorDetail.blood_group,
                    DonorDetail.personal_details_id,
                    DonorDetail.active_status,
                    DonorDetail.last_donated_date,
                    DonorDetail.number_of_times_donated,
                    DonorDetail.last_login_date,
                    PersonalDetailsUser.first_name,
                    PersonalDetailsUser.last_name,
                    PersonalDetailsUser.age,
                    PersonalDetailsUser.contact_number,
                    PersonalDetailsUser.date_of_birth,
                    PersonalDetailsUser.marital_status,
                    PersonalDetailsUser.secondary_contact_number,
                    PersonalDetailsUser.aadhar_number,
                    AddressDetailsUser.address,
                    AddressDetailsUser.city,
                    AddressDetailsUser.country,
                    AddressDetailsUser.state,
                    AddressDetailsUser.pincode,
                    DiseaseDetailsUser.name.label('disease_name'),
                    DiseaseDetailsUser.description.label('disease_description')
                )
                .join(PersonalDetailsUser , DonorDetail.personal_details_id==PersonalDetailsUser.id)
                .join(AddressDetailsUser , DonorDetail.address_id == AddressDetailsUser.id)
                .join(DiseaseDetailsUser , DonorDetail.disease_id == DiseaseDetailsUser.id)
                .filter(DonorDetail.id == donor_id)
                .first()
            )
            return donor_detail
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    @staticmethod
    def fetch_donor_detail_by_blood_group(blood_group):
        try:
            donor_details = (
                db.session.query(
                    DonorDetail.id,
                    DonorDetail.name,
                    DonorDetail.email,
                    DonorDetail.blood_group,
                    DonorDetail.active_status
                )
                .filter(DonorDetail.blood_group == blood_group)
                .all()
            )
            return donor_details
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    @staticmethod
    def fetch_donor_detail_by_name(name):
        try:
            donor_details = (
                db.session.query(
                    DonorDetail.id,
                    DonorDetail.name,
                    DonorDetail.email,
                    DonorDetail.blood_group,
                    DonorDetail.active_status
                )
                .filter(DonorDetail.name.ilike(f"%{name}%"))
                .all()
            )
            return donor_details
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    @staticmethod
    def fetch_donor_detail_by_blood_group_and_name(name,blood_group):
        try:
            donor_details = (
                db.session.query(
                    DonorDetail.id,
                    DonorDetail.name,
                    DonorDetail.email,
                    DonorDetail.blood_group,
                    DonorDetail.active_status
                )
                .filter(DonorDetail.blood_group == blood_group, DonorDetail.name.ilike(f'%{name}%'))  # Filters by both blood group and name
                .all()
            )
            return donor_details
        except Exception as e:
            print(f"An error occurred: {e}")
            raise
    

    @staticmethod
    def fetch_admin_details(admin_id):
        try:
            admin_details = (
                db.session.query(
                    AdminDetails.id,
                    AdminDetails.email,
                    AdminDetails.password,
                    AdminDetails.username,
                    AdminDetails.vec_registration_number,
                    AdminDetails.data_of_birth,
                    AdminDetails.mobile_number,
                    AdminDetails.department,
                    AdminDetails.active_status,
                    AdminDetails.approved_donation_count,
                    AdminDetails.closed_requests_count
                )
                .filter(AdminDetails.id == admin_id)
                .first()
            )
            return admin_details
        except Exception as e:
            print(f"An error occurred: {e}")
            raise
  
    @staticmethod
    def generate_analytics():
        donor_results = db.session.query(
            DonorDetail.blood_group,
            func.count().label("total_count"),
            func.sum(func.if_(DonorDetail.active_status, 1, 0)).label("active_count"),
            func.sum(func.if_(~DonorDetail.active_status, 1, 0)).label("inactive_count")
        ).group_by(DonorDetail.blood_group).all()

        statuses_response = ['Success', 'Partial Success', 'Failure', 'Pending','Declined']
        status_counts = {status: 0 for status in statuses_response}

        # Query for status counts
        results = db.session.query(
            ResponseDetails.status,
            func.count(ResponseDetails.id).label('count')
        ).group_by(ResponseDetails.status).all()

        for result in results:
            status = result.status if result.status else 'Pending'
            if status in status_counts:
                status_counts[status] += result.count

        plt.figure(figsize=(8, 5))
        plt.bar(status_counts.keys(), status_counts.values(), color=['green', 'orange', 'red', 'blue','skyblue'])
        plt.xlabel('Response Status')
        plt.ylabel('Count')
        plt.title('Response Status Distribution')

        image_path = os.path.join("app/static/images/admin_analytics", "response_status_distribution.png")
        plt.savefig(image_path)
        plt.close()

        blood_groups = [result.blood_group for result in donor_results]
        active_counts = [result.active_count for result in donor_results]
        inactive_counts = [result.inactive_count for result in donor_results]

        statuses = ['Closed', 'Not_Approved', 'Expired', 'Pending']
        counts = {status: db.session.query(BloodRequestDetails).filter_by(status=status).count() for status in statuses}

        plt.figure(figsize=(10, 6))
        x = range(len(blood_groups))
        plt.bar(x, active_counts, width=0.4, label="Active Donors", color="skyblue", align='center')
        plt.bar(x, inactive_counts, width=0.4, label="Inactive Donors", color="salmon", align='edge')
        plt.xlabel("Blood Group")
        plt.ylabel("Number of Donors")
        plt.title("Donor Analytics by Blood Group")
        plt.xticks(x, blood_groups)
        plt.legend()

        image_path = os.path.join("app/static/images/admin_analytics", "donor_analytics_chart.png")
        plt.savefig(image_path)
        plt.close()

        plt.figure(figsize=(8, 5))
        plt.bar(counts.keys(), counts.values(), color=['green', 'red', 'orange', 'blue'])
        plt.xlabel('Request Status')
        plt.ylabel('Count')
        plt.title('Blood Request Status Distribution')
        
        image_path = os.path.join("app/static/images/admin_analytics", "blood_request_status.png")
        plt.savefig(image_path)
        plt.close()

        hospital_count = db.session.query(HospitalDetails).count()

        last_30_days = datetime.now() - timedelta(days=30)

        recent_donor_count = db.session.query(DonorDetail).filter(
            DonorDetail.last_login_date >= last_30_days
        ).count()

        recent_request_count = db.session.query(BloodRequestDetails).filter(
            BloodRequestDetails.due_date >= last_30_days
        ).count()

        return {
            'hospital_count': hospital_count,
            'recent_donor_count': recent_donor_count,
            'recent_request_count': recent_request_count
        }
    
    @staticmethod
    def fetch_all_donors():
        donors = db.session.query(
            DonorDetail.id,
            DonorDetail.name,
            DonorDetail.email,
            DonorDetail.blood_group,
            DonorDetail.active_status
        ).all()
        return donors
    
    @staticmethod
    def fetch_all_hospitals():
        hospitals = db.session.query(
            HospitalDetails.id,
            HospitalDetails.hospital_name,
            HospitalDetails.city,
            HospitalDetails.state
        ).all()
        return hospitals
    
    @staticmethod
    def fetch_hospital_detail(hospital_id):
        try:
            hospital_details = (
                db.session.query(
                    HospitalDetails.id,
                    HospitalDetails.hospital_name,
                    HospitalDetails.hospital_address,
                    HospitalDetails.city,
                    HospitalDetails.state,
                    HospitalDetails.country,
                    HospitalDetails.pincode,
                    HospitalDetails.branch,
                    HospitalDetails.landmark
                )
                .filter(HospitalDetails.id == hospital_id)
                .first()
            )
            return hospital_details
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    @staticmethod
    def fetch_hospital_details_autofill():
        try:
            hospital_details = (
                db.session.query(
                    HospitalDetails.id,
                    HospitalDetails.hospital_name,
                    HospitalDetails.hospital_address
                ).all()
            )

            hospital_data = [
                {
                    "id": hospital.id,
                    "name": hospital.hospital_name,
                    "address": hospital.hospital_address
                }
                for hospital in hospital_details
            ]
            
            with open('app/static/json_files/hospital_details.json', 'w') as json_file:
                json.dump(hospital_data, json_file, indent=4)

        except Exception as e:
            print(f"An error occurred: {e}")
            raise


    @staticmethod
    def generate_notifications():
        try:
            counts = db.session.query(
                func.count(BloodRequestDetails.id).label('count'),
                BloodRequestDetails.status
            ).filter(
                BloodRequestDetails.status.in_(['Not_Approved', 'Pending', 'Expired'])
            ).group_by(
                BloodRequestDetails.status
            ).all()
            status_counts = {'Not_Approved': 0, 'Pending': 0, 'Expired': 0}
            for row in counts:
                status_counts[row.status] = row.count

            active_donors_count = db.session.query(
                func.count(DonorDetail.id)
            ).filter(DonorDetail.active_status==True).scalar()

            Inactive_donors_count = db.session.query(
                func.count(DonorDetail.id)
            ).filter(DonorDetail.active_status==False).scalar()

            Total_Requests = db.session.query(
                func.count(BloodRequestDetails.id)
            ).scalar()

            return status_counts , active_donors_count , Inactive_donors_count , Total_Requests
        except Exception as e:
            print(f"An error occurred: {e}")
            raise