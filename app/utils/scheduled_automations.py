from app.models import db, BloodRequestDetails
from datetime import date

def expire_blood_requests():
    try:
        # Retrieve current date
        current_date = date.today()

        # Query for expired requests
        expired_requests = (
            db.session.query(BloodRequestDetails)
            .filter(
                BloodRequestDetails.status.in_(['Pending', 'Not_Approved']),
                BloodRequestDetails.due_date < current_date
            )
            .all()
        )

        # Update status to 'Expired'
        for request in expired_requests:
            request.status = 'Expired'

        db.session.commit()
        print(f"{len(expired_requests)} blood request(s) expired successfully.")

    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while expiring requests: {e}")


def increment_age():
    print("Age incremented")
