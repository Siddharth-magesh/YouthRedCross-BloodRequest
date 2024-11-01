from app.models import BloodRequestDetails, HospitalDetails, DonorDetail, ResponseDetails, PersonalDetailsUser , AddressDetailsUser, DiseaseDetailsUser,db

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
                # Adding the subquery to count active donors
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
                db.session.commit()
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
                ResponseDetails.status.label("response_status"),
                ResponseDetails.report,
                ResponseDetails.units_donated,
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
                ResponseDetails.status.label("response_status"),
                ResponseDetails.report,
                ResponseDetails.units_donated,
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
                ResponseDetails.status.label("response_status"),
                ResponseDetails.report,
                ResponseDetails.units_donated,
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
    def update_expired_request(request_id,response_status,report,units_donated,response_donor_ids):
        try:
            blood_request = BloodRequestDetails.query.filter_by(id=request_id).first()
            if not blood_request:
                raise ValueError("Blood request with the given ID does not exist.")

            blood_request.status = "Closed"

            response_detail = ResponseDetails.query.filter_by(id=blood_request.response_id).first()
            if response_detail:
                response_detail.status = response_status
                response_detail.report = report
                response_detail.units_donated = units_donated
                response_detail.donor_ids = response_donor_ids
            else:
                raise ValueError("No response found for the given blood request.")

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")
            raise

    @staticmethod
    def update_ongoing_request(request_id,response_status,report,units_donated,response_donor_ids):
        try:
            blood_request = BloodRequestDetails.query.filter_by(id=request_id).first()
            if not blood_request:
                raise ValueError("Blood request with the given ID does not exist.")

            blood_request.status = "Closed"

            response_detail = ResponseDetails.query.filter_by(id=blood_request.response_id).first()
            if response_detail:
                response_detail.status = response_status
                response_detail.report = report
                response_detail.units_donated = units_donated
                response_detail.donor_ids = response_donor_ids
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