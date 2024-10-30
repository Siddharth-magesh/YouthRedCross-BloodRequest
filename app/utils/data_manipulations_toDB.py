from app.models import BloodRequestDetails, HospitalDetails, DonorDetail, ResponseDetails,db

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