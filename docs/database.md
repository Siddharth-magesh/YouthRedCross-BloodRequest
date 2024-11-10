# Database Structure for Youth Red Cross Blood Donation Site

This document describes the database schema, including tables, columns, primary keys, and relationships between tables.

## Table Structure Overview

| Table Name                 | Primary Key | Description                                        |
| -------------------------- | ----------- | -------------------------------------------------- |
| DonorDetail                | id          | Stores information about donors.                   |
| AuthenticationDetailsDonor | id          | Logs donor login details.                          |
| PersonalDetailsUser        | id          | Stores personal details of each user.              |
| AddressDetailsUser         | id          | Stores address information of each user.           |
| DiseaseDetailsUser         | id          | Records diseases associated with users.            |
| AdminDetails               | id          | Stores information about admin users.              |
| AuthenticationDetailsAdmin | id          | Logs admin login details.                          |
| BloodRequestDetails        | id          | Holds details of blood requests made by patients.  |
| HospitalDetails            | id          | Stores information about hospitals.                |
| ResponseDetails            | id          | Contains responses and statuses of blood requests. |

## Detailed Table Structure and Relationships

### DonorDetail

| Column                  | Type         | Description                                      |
| ----------------------- | ------------ | ------------------------------------------------ |
| id                      | VARCHAR(36)  | Primary Key, unique identifier for each donor.   |
| name                    | VARCHAR(100) | Donor's name.                                    |
| email                   | VARCHAR(100) | Donor's email (unique).                          |
| password                | VARCHAR(500) | Hashed password for donor login.                 |
| blood_group             | VARCHAR(10)  | Donor's blood group.                             |
| personal_details_id     | VARCHAR(36)  | Foreign Key referencing `PersonalDetailsUser.id` |
| address_id              | VARCHAR(36)  | Foreign Key referencing `AddressDetailsUser.id`  |
| active_status           | BOOLEAN      | Indicates if donor is active.                    |
| disease_id              | VARCHAR(36)  | Foreign Key referencing `DiseaseDetailsUser.id`  |
| authentication_id       | VARCHAR(36)  | Unique ID for donor authentication.              |
| last_donated_date       | DateTime     | Date of last donation.                           |
| number_of_times_donated | INT          | Number of donations made by donor.               |
| last_login_date         | DateTime     | Date of last login.                              |

- **Relationships**:
  - `personal_details_id` links to `PersonalDetailsUser.id`.
  - `address_id` links to `AddressDetailsUser.id`.
  - `disease_id` links to `DiseaseDetailsUser.id`.

### AuthenticationDetailsDonor

| Column     | Type         | Description                                 |
| ---------- | ------------ | ------------------------------------------- |
| id         | INT          | Primary Key.                                |
| auth_id    | VARCHAR(36)  | References `DonorDetail.authentication_id`. |
| name       | VARCHAR(100) | Name of donor.                              |
| login_date | Date         | Date of login.                              |
| login_time | Time         | Time of login.                              |

### PersonalDetailsUser

| Column                   | Type        | Description                   |
| ------------------------ | ----------- | ----------------------------- |
| id                       | VARCHAR(36) | Primary Key.                  |
| first_name               | VARCHAR(45) | Donor's first name.           |
| last_name                | VARCHAR(45) | Donor's last name.            |
| age                      | INT         | Donor's age.                  |
| date_of_birth            | Date        | Donor's date of birth.        |
| contact_number           | VARCHAR(15) | Primary contact number.       |
| secondary_contact_number | VARCHAR(15) | Secondary contact (optional). |
| marital_status           | VARCHAR(10) | Marital status (optional).    |
| aadhar_number            | VARCHAR(20) | Aadhaar ID (optional).        |

### AddressDetailsUser

| Column  | Type         | Description     |
| ------- | ------------ | --------------- |
| id      | VARCHAR(36)  | Primary Key.    |
| address | VARCHAR(200) | Street address. |
| pincode | VARCHAR(10)  | Postal code.    |
| country | VARCHAR(45)  | Country.        |
| state   | VARCHAR(45)  | State.          |
| city    | VARCHAR(45)  | City.           |

### DiseaseDetailsUser

| Column      | Type         | Description                       |
| ----------- | ------------ | --------------------------------- |
| id          | VARCHAR(36)  | Primary Key.                      |
| name        | VARCHAR(100) | Disease name.                     |
| description | VARCHAR(200) | Additional details about disease. |

### AdminDetails

| Column                  | Type         | Description                         |
| ----------------------- | ------------ | ----------------------------------- |
| id                      | VARCHAR(36)  | Primary Key.                        |
| email                   | VARCHAR(100) | Admin's email (unique).             |
| password                | VARCHAR(250) | Hashed password for admin login.    |
| username                | VARCHAR(45)  | Admin's username.                   |
| authentication_id       | VARCHAR(36)  | Unique ID for admin authentication. |
| vec_registration_number | VARCHAR(36)  | Admin's unique registration number. |
| date_of_birth           | Date         | Admin's date of birth.              |
| mobile_number           | VARCHAR(36)  | Contact number.                     |
| department              | VARCHAR(50)  | Admin's department (optional).      |
| active_status           | VARCHAR(36)  | Status of admin (active/inactive).  |
| last_login_date         | DateTime     | Date of last login.                 |
| approved_donation       | VARCHAR(36)  | Number of approved donations.       |
| closed_requests         | VARCHAR(36)  | Number of closed requests.          |

### AuthenticationDetailsAdmin

| Column     | Type         | Description                                  |
| ---------- | ------------ | -------------------------------------------- |
| id         | INT          | Primary Key.                                 |
| auth_id    | VARCHAR(36)  | References `AdminDetails.authentication_id`. |
| name       | VARCHAR(100) | Name of admin.                               |
| login_date | Date         | Date of login.                               |
| login_time | Time         | Time of login.                               |

### BloodRequestDetails

| Column            | Type         | Description                                        |
| ----------------- | ------------ | -------------------------------------------------- |
| id                | VARCHAR(36)  | Primary Key.                                       |
| patient_name      | VARCHAR(100) | Name of the patient.                               |
| blood_group       | VARCHAR(10)  | Required blood group.                              |
| hospital_name     | VARCHAR(100) | Name of hospital.                                  |
| hospital_id       | VARCHAR(36)  | Foreign Key referencing `HospitalDetails.id`.      |
| contact_number    | VARCHAR(15)  | Contact number of requestor.                       |
| patient_age       | INT          | Patient’s age.                                     |
| due_date          | DateTime     | Date by which blood is needed.                     |
| request_reason    | VARCHAR(200) | Reason for request (optional).                     |
| status            | VARCHAR(45)  | Status of the request (open/closed).               |
| units_required    | INT          | Number of blood units required.                    |
| attendant_name    | VARCHAR(100) | Name of attendant (optional).                      |
| response_id       | VARCHAR(36)  | Foreign Key referencing `ResponseDetails.id`.      |
| approved_admin_id | VARCHAR(36)  | Admin ID who approved (session managed).           |
| closed_admin_id   | VARCHAR(36)  | Admin ID who closed the request (session managed). |

### HospitalDetails

| Column           | Type         | Description                 |
| ---------------- | ------------ | --------------------------- |
| id               | VARCHAR(36)  | Primary Key.                |
| hospital_name    | VARCHAR(100) | Name of the hospital.       |
| hospital_address | VARCHAR(200) | Address of the hospital.    |
| pincode          | VARCHAR(10)  | Postal code.                |
| city             | VARCHAR(45)  | City.                       |
| state            | VARCHAR(45)  | State.                      |
| country          | VARCHAR(45)  | Country.                    |
| branch           | VARCHAR(45)  | Branch name (optional).     |
| landmark         | VARCHAR(100) | Nearby landmark (optional). |

### ResponseDetails

| Column             | Type         | Description                               |
| ------------------ | ------------ | ----------------------------------------- |
| id                 | VARCHAR(36)  | Primary Key.                              |
| status             | VARCHAR(45)  | Current status of response.               |
| report             | VARCHAR(255) | Report on the response (optional).        |
| units_donated      | INT          | Number of units donated.                  |
| certificate_status | VARCHAR(36)  | Certificate status (generated/pending).   |
| donor_ids          | VARCHAR(255) | IDs of donors involved (comma-separated). |

---

## Relationships

1. **`DonorDetail` Table**:

   - `personal_details_id` -> `PersonalDetailsUser.id`
   - `address_id` -> `AddressDetailsUser.id`
   - `disease_id` -> `DiseaseDetailsUser.id`

2. \*\*`BloodRequestDetails` Table

\*\*:

- `hospital_id` -> `HospitalDetails.id`
- `response_id` -> `ResponseDetails.id`

## Primary Key IDs:

1. **PersonalDetailsUser**: `id` (e.g., `PDDNR001`)
2. **AddressDetailsUser**: `id` (e.g., `ADDR001`)
3. **DiseaseDetailsUser**: `id` (e.g., `DIS001`)
4. **AuthenticationDetailsAdmin**: `id` (e.g., `AUTHADM001`)
5. **AdminDetails**: `id` (e.g., `ADMIN001`)
6. **HospitalDetails**: `id` (e.g., `HOSP001`)
7. **ResponseDetails**: `id` (e.g., `RESP001`)
8. **BloodRequestDetails**: `id` (e.g., `BR001`)
9. **AuthenticationDetailsDonor**: `id` (e.g., `AUTHDNR001`)
10. **DonorDetail**: `id` (e.g., `DNR001`)

## Primary Key Id Generation Function

```bash
def get_next_id(table, prefix):
    # Fetch the current maximum ID, strip the prefix and convert to an integer
    max_id = db.session.query(table.id).order_by(table.id.desc()).first()
    next_id_num = 1
    if max_id:
        # Extract the numeric part of the ID
        current_num = int(max_id[0][len(prefix):])
        next_id_num = current_num + 1
    # Format the new ID
    return f"{prefix}{str(next_id_num).zfill(3)}"

#Call This function to generate the next ID for the Following table you have passed
personal_id = get_next_id(PersonalDetailsUser, 'PDDNR')
```
