# Database Structure for Youth Red Cross Blood Donation Site

This document describes the database schema for the Youth Red Cross Blood Donation Site, including tables, columns, primary keys, and relationships between tables.

---

## Table Structure Overview

| Table Name                 | Primary Key Format | Description                                        |
| -------------------------- | ------------------ | -------------------------------------------------- |
| DonorDetail                | DNR###             | Stores information about donors.                   |
| TermsAndConditions         | TNC###             | Contains terms and conditions details.             |
| AuthenticationDetailsDonor | AUTHDNR###         | Logs donor authentication details.                 |
| PersonalDetailsUser        | PDDNR###           | Stores personal details of each donor.             |
| AddressDetailsUser         | ADDR###            | Stores address information of donors.              |
| DiseaseDetailsUser         | DIS###             | Records diseases associated with donors.           |
| AdminDetails               | ADMIN###           | Stores information about admin users.              |
| AuthenticationDetailsAdmin | AUTHADM###         | Logs admin authentication details.                 |
| BloodRequestDetails        | BR###              | Holds details of blood requests made by patients.  |
| HospitalDetails            | HOSP###            | Stores information about hospitals.                |
| ResponseDetails            | RESP###            | Contains responses and statuses of blood requests. |
| QueryTable                 | AUTO_INCREMENT     | Logs user queries and admin responses.             |

---

## Detailed Table Structure and Relationships

### DonorDetail

| Column                  | Type         | Description                                                     |
| ----------------------- | ------------ | --------------------------------------------------------------- |
| id                      | VARCHAR(36)  | Primary Key, unique identifier for each donor (e.g., `DNR001`). |
| name                    | VARCHAR(100) | Donor's name.                                                   |
| email                   | VARCHAR(100) | Donor's email (unique).                                         |
| password                | VARCHAR(500) | Hashed password for donor login.                                |
| blood_group             | VARCHAR(10)  | Donor's blood group.                                            |
| personal_details_id     | VARCHAR(36)  | Foreign Key referencing `PersonalDetailsUser.id`.               |
| terms_and_conditions_id | VARCHAR(36)  | Foreign Key referencing `TermsAndConditions.id`.                |
| address_id              | VARCHAR(36)  | Foreign Key referencing `AddressDetailsUser.id`.                |
| active_status           | BOOLEAN      | Indicates if donor is active.                                   |
| disease_id              | VARCHAR(36)  | Foreign Key referencing `DiseaseDetailsUser.id`.                |
| authentication_id       | VARCHAR(36)  | Unique ID for donor authentication.                             |
| last_donated_date       | DateTime     | Date of last donation.                                          |
| number_of_times_donated | INT          | Number of donations made by donor.                              |
| last_login_date         | DateTime     | Date of last login.                                             |

- **Relationships**:
  - `personal_details_id` -> `PersonalDetailsUser.id`
  - `terms_and_conditions_id` -> `TermsAndConditions.id`
  - `address_id` -> `AddressDetailsUser.id`
  - `disease_id` -> `DiseaseDetailsUser.id`

---

### TermsAndConditions

| Column         | Type        | Description                   |
| -------------- | ----------- | ----------------------------- |
| id             | VARCHAR(36) | Primary Key (e.g., `TNC001`). |
| version        | VARCHAR(20) | Version of the terms.         |
| effective_date | Date        | Effective date of the terms.  |

---

### AuthenticationDetailsDonor

| Column     | Type         | Description                                 |
| ---------- | ------------ | ------------------------------------------- |
| id         | INT          | Primary Key (e.g., `AUTHDNR001`).           |
| auth_id    | VARCHAR(36)  | References `DonorDetail.authentication_id`. |
| name       | VARCHAR(100) | Name of donor.                              |
| login_date | Date         | Date of login.                              |
| login_time | Time         | Time of login.                              |

---

### PersonalDetailsUser

| Column                   | Type        | Description                     |
| ------------------------ | ----------- | ------------------------------- |
| id                       | VARCHAR(36) | Primary Key (e.g., `PDDNR001`). |
| first_name               | VARCHAR(45) | Donor's first name.             |
| last_name                | VARCHAR(45) | Donor's last name.              |
| age                      | INT         | Donor's age.                    |
| date_of_birth            | Date        | Donor's date of birth.          |
| contact_number           | VARCHAR(15) | Primary contact number.         |
| secondary_contact_number | VARCHAR(15) | Secondary contact (optional).   |
| marital_status           | VARCHAR(10) | Marital status (optional).      |
| aadhar_number            | VARCHAR(20) | Aadhaar ID (optional).          |

---

### AddressDetailsUser

| Column  | Type         | Description                    |
| ------- | ------------ | ------------------------------ |
| id      | VARCHAR(36)  | Primary Key (e.g., `ADDR001`). |
| address | VARCHAR(200) | Street address.                |
| pincode | VARCHAR(10)  | Postal code.                   |
| country | VARCHAR(45)  | Country.                       |
| state   | VARCHAR(45)  | State.                         |
| city    | VARCHAR(45)  | City.                          |

---

### DiseaseDetailsUser

| Column      | Type         | Description                       |
| ----------- | ------------ | --------------------------------- |
| id          | VARCHAR(36)  | Primary Key (e.g., `DIS001`).     |
| name        | VARCHAR(100) | Disease name.                     |
| description | VARCHAR(200) | Additional details about disease. |

---

### AdminDetails

| Column                  | Type         | Description                         |
| ----------------------- | ------------ | ----------------------------------- |
| id                      | VARCHAR(36)  | Primary Key (e.g., `ADMIN001`).     |
| email                   | VARCHAR(100) | Admin's email (unique).             |
| password                | VARCHAR(250) | Hashed password for admin login.    |
| username                | VARCHAR(45)  | Admin's username.                   |
| authentication_id       | VARCHAR(36)  | Unique ID for admin authentication. |
| vec_registration_number | VARCHAR(36)  | Admin's unique registration number. |
| data_of_birth           | Date         | Admin's date of birth.              |
| mobile_number           | VARCHAR(36)  | Contact number.                     |
| department              | VARCHAR(50)  | Admin's department (optional).      |
| active_status           | VARCHAR(36)  | Status of admin (active/inactive).  |
| last_login_date         | DateTime     | Date of last login.                 |
| approved_donation_count | INT          | Number of approved donations.       |
| closed_requests_count   | INT          | Number of closed requests.          |

- **Relationships**:
  - None explicitly defined.

---

### BloodRequestDetails

| Column            | Type         | Description                                        |
| ----------------- | ------------ | -------------------------------------------------- |
| id                | VARCHAR(36)  | Primary Key (e.g., `BR001`).                       |
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

- **Relationships**:
  - `hospital_id` -> `HospitalDetails.id`
  - `response_id` -> `ResponseDetails.id`

---

### Relationships Summary

1. **`DonorDetail` Table**:

   - Links to `PersonalDetailsUser.id`, `TermsAndConditions.id`, `AddressDetailsUser.id`, `DiseaseDetailsUser.id`.

2. **`BloodRequestDetails` Table**:

   - Links to `HospitalDetails.id`, `ResponseDetails.id`.

3. **Authentication and Terms**:
   - Separate tables to manage donor and admin authentication and terms & conditions.
