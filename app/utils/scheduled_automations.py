from app.models import db, BloodRequestDetails , PersonalDetailsUser , DonorDetail
from datetime import date , datetime , timedelta

def expire_blood_requests():
    try:
        current_date = date.today()

        expired_requests = (
            db.session.query(BloodRequestDetails)
            .filter(
                BloodRequestDetails.status.in_(['Pending', 'Not_Approved']),
                BloodRequestDetails.due_date < current_date
            )
            .all()
        )

        for request in expired_requests:
            request.status = 'Expired'

        db.session.commit()
        print(f"{len(expired_requests)} blood request(s) expired successfully.")

    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while expiring requests: {e}")


from datetime import datetime

def increment_age():
    current_date = datetime.now().date()
    
    donors = DonorDetail.query.all()
    
    for donor in donors:
        personal_details = PersonalDetailsUser.query.filter_by(id=donor.personal_details_id).first()
        
        if personal_details:
            dob = personal_details.date_of_birth
            
            if dob.month == current_date.month and dob.day == current_date.day:
                personal_details.age += 1
                db.session.commit()
                
                print(f"Donor {donor.name}'s age has been incremented to {personal_details.age}.")

def activate_donor_status():
    try:
        current_date = datetime.now().date()
        
        two_months_ago = current_date - timedelta(days=60)

        inactive_donors = db.session.query(DonorDetail).filter(
            DonorDetail.active_status == False,
            DonorDetail.last_donated_date <= two_months_ago
        ).all()

        for donor in inactive_donors:
            donor.active_status = True

        db.session.commit()

        print(f"Activated {len(inactive_donors)} donors whose last donation was over two months ago.")

    except Exception as e:
        print(f"An error occurred while activating donor statuses: {e}")
        db.session.rollback()
        raise
   