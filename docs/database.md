# Youth Red Cross Blood Request Database Documentation

## Database: `YouthRedCross_BloodRequest`

This database is designed to manage blood donation requests, donor records, hospital information, and other relevant details for the Youth Red Cross Blood Request system. Below are detailed descriptions of each table, its columns, and the relationships between tables.

---

### Table: `PersonalDetailsUser`

Stores personal details of users.

| Column                     | Type        | Description                           |
| -------------------------- | ----------- | ------------------------------------- |
| `id`                       | INT         | Primary key, unique identifier.       |
| `first_name`               | VARCHAR(45) | First name of the user.               |
| `last_name`                | VARCHAR(45) | Last name of the user.                |
| `age`                      | INT         | Age of the user.                      |
| `date_of_birth`            | DATE        | Date of birth of the user.            |
| `contact_number`           | VARCHAR(15) | Primary contact number of the user.   |
| `secondary_contact_number` | VARCHAR(15) | Secondary contact number (optional).  |
| `marital_status`           | VARCHAR(10) | Marital status of the user.           |
| `aadhar_number`            | VARCHAR(20) | Aadhar number of the user (optional). |

---

### Table: `AddressDetailsUser`

Stores address information for users.

| Column    | Type         | Description                     |
| --------- | ------------ | ------------------------------- |
| `id`      | INT          | Primary key, unique identifier. |
| `address` | VARCHAR(200) | Full address of the user.       |
| `pincode` | VARCHAR(10)  | Postal code for the address.    |
| `country` | VARCHAR(45)  | Country of residence.           |
| `state`   | VARCHAR(45)  | State or province of residence. |
| `city`    | VARCHAR(45)  | City of residence.              |

---

### Table: `DiseaseDetailsUser`

Stores disease information.

| Column        | Type         | Description                       |
| ------------- | ------------ | --------------------------------- |
| `id`          | INT          | Primary key, unique identifier.   |
| `name`        | VARCHAR(100) | Name of the disease or condition. |
| `description` | VARCHAR(200) | Description of the disease.       |

---

### Table: `DonorDetail`

Stores information about blood donors, including their personal and address details.

| Column                | Type         | Description                                        |
| --------------------- | ------------ | -------------------------------------------------- |
| `id`                  | INT          | Primary key, unique identifier.                    |
| `name`                | VARCHAR(100) | Name of the donor.                                 |
| `blood_group`         | VARCHAR(10)  | Blood group of the donor.                          |
| `personal_details_id` | INT          | Foreign key referencing `PersonalDetailsUser(id)`. |
| `address_id`          | INT          | Foreign key referencing `AddressDetailsUser(id)`.  |
| `active_status`       | BOOLEAN      | Indicates if the donor is actively donating.       |
| `disease_id`          | INT          | Foreign key referencing `DiseaseDetailsUser(id)`.  |
| `last_donated_date`   | DATETIME     | Date of the last blood donation.                   |

---

### Table: `AdminDetails`

Stores administrator details.

| Column              | Type         | Description                                            |
| ------------------- | ------------ | ------------------------------------------------------ |
| `id`                | INT          | Primary key, unique identifier.                        |
| `email`             | VARCHAR(100) | Email of the admin.                                    |
| `password`          | VARCHAR(100) | Encrypted password.                                    |
| `username`          | VARCHAR(45)  | Username for the admin account.                        |
| `last_login_date`   | DATETIME     | Timestamp of the last login.                           |
| `approved_donation` | BOOLEAN      | Indicates if the admin has approved donation requests. |

---

### Table: `AuthenticationDetailsAdmin`

Stores authentication logs for admins.

| Column       | Type         | Description                                 |
| ------------ | ------------ | ------------------------------------------- |
| `admin_id`   | INT          | Foreign key referencing `AdminDetails(id)`. |
| `name`       | VARCHAR(100) | Name of the admin logging in.               |
| `login_date` | DATE         | Date of login.                              |
| `login_time` | TIME         | Time of login.                              |

---

### Table: `HospitalDetails`

Stores information about hospitals.

| Column             | Type         | Description                            |
| ------------------ | ------------ | -------------------------------------- |
| `id`               | INT          | Primary key, unique identifier.        |
| `hospital_name`    | VARCHAR(100) | Name of the hospital.                  |
| `hospital_address` | VARCHAR(200) | Address of the hospital.               |
| `pincode`          | VARCHAR(10)  | Postal code of the hospital.           |
| `city`             | VARCHAR(45)  | City where the hospital is located.    |
| `state`            | VARCHAR(45)  | State where the hospital is located.   |
| `country`          | VARCHAR(45)  | Country where the hospital is located. |
| `branch`           | VARCHAR(45)  | Branch name if applicable.             |
| `landmark`         | VARCHAR(100) | Nearby landmark if applicable.         |

---

### Table: `BloodRequestDetails`

Stores blood donation requests.

| Column           | Type         | Description                                    |
| ---------------- | ------------ | ---------------------------------------------- |
| `id`             | INT          | Primary key, unique identifier.                |
| `patient_name`   | VARCHAR(100) | Name of the patient.                           |
| `blood_group`    | VARCHAR(10)  | Required blood group.                          |
| `hospital_name`  | VARCHAR(100) | Name of the hospital.                          |
| `hospital_id`    | INT          | Foreign key referencing `HospitalDetails(id)`. |
| `contact_number` | VARCHAR(15)  | Contact number for the request.                |
| `patient_age`    | INT          | Age of the patient.                            |
| `due_date`       | DATETIME     | Due date for the blood requirement.            |
| `request_reason` | VARCHAR(200) | Reason for the blood request.                  |
| `status`         | VARCHAR(45)  | Status of the request.                         |
| `units_required` | INT          | Number of units required.                      |
| `attendant_name` | VARCHAR(100) | Name of the attendant.                         |
| `donor_ids`      | VARCHAR(255) | IDs of donors who donated (JSON-like).         |
| `response_id`    | INT          | Foreign key referencing `ResponseDetails(id)`. |

---

### Table: `ResponseDetails`

Stores responses to blood donation requests.

| Column             | Type         | Description                                        |
| ------------------ | ------------ | -------------------------------------------------- |
| `id`               | INT          | Primary key, unique identifier.                    |
| `blood_request_id` | INT          | Foreign key referencing `BloodRequestDetails(id)`. |
| `status`           | VARCHAR(45)  | Status of the response.                            |
| `report`           | VARCHAR(255) | Report of the donation.                            |
| `units_donated`    | INT          | Number of units donated.                           |
| `donor_ids`        | VARCHAR(255) | IDs of donors who donated (JSON-like).             |

---

## Relationships

- **One-to-Many Relationships**:

  - `PersonalDetailsUser` to `DonorDetail`
  - `AddressDetailsUser` to `DonorDetail`
  - `AdminDetails` to `AuthenticationDetailsAdmin`
  - `HospitalDetails` to `BloodRequestDetails`
  - `BloodRequestDetails` to `ResponseDetails`

- **Many-to-One Relationships**:
  - `DonorDetail` to `DiseaseDetailsUser`
  - `DonorDetail` to `AddressDetailsUser`
  - `ResponseDetails` to `BloodRequestDetails`

---

## Usage

This schema provides comprehensive management capabilities for donor details, blood requests, and response tracking. Each table is optimized for relational integrity, allowing for seamless tracking of donors and requests across the Youth Red Cross system.
