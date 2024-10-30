# Youth Red Cross Blood Request Database Documentation

## Database: `YouthRedCross_BloodRequest`

This database is designed to manage blood donation requests, donor records, hospital information, and other related data. Below are detailed descriptions of each table, including columns, data types, and relationships.

---

### Table: `PersonalDetailsUser`

**Purpose**: Stores personal information about users.

| Column                     | Type        | Description                                        |
| -------------------------- | ----------- | -------------------------------------------------- |
| `id`                       | VARCHAR(10) | Primary key, unique identifier (e.g., `PDDNR001`). |
| `first_name`               | VARCHAR(45) | First name of the user.                            |
| `last_name`                | VARCHAR(45) | Last name or initial of the user.                  |
| `age`                      | INT         | Age of the user.                                   |
| `date_of_birth`            | DATE        | Date of birth of the user.                         |
| `contact_number`           | VARCHAR(15) | Primary contact number of the user.                |
| `secondary_contact_number` | VARCHAR(15) | Secondary contact number (optional).               |
| `marital_status`           | VARCHAR(10) | Marital status of the user (optional).             |
| `aadhar_number`            | VARCHAR(20) | Aadhar number (optional).                          |
| `blood_group`              | VARCHAR(10) | Blood group of the user.                           |
| `last_donated_date`        | DATE        | Date of last donation (optional).                  |

---

### Table: `AddressDetailsUser`

**Purpose**: Stores address information for users.

| Column    | Type         | Description                                       |
| --------- | ------------ | ------------------------------------------------- |
| `id`      | VARCHAR(10)  | Primary key, unique identifier (e.g., `ADDR001`). |
| `address` | VARCHAR(200) | Full address (address, city, state, pincode).     |
| `pincode` | VARCHAR(10)  | Postal code for the address.                      |
| `country` | VARCHAR(45)  | Country of residence.                             |
| `state`   | VARCHAR(45)  | State or province of residence.                   |
| `city`    | VARCHAR(45)  | City of residence.                                |

---

### Table: `DiseaseDetailsUser`

**Purpose**: Stores disease information for users, if applicable.

| Column        | Type         | Description                                      |
| ------------- | ------------ | ------------------------------------------------ |
| `id`          | VARCHAR(10)  | Primary key, unique identifier (e.g., `DIS001`). |
| `name`        | VARCHAR(100) | Name of the disease or condition.                |
| `description` | VARCHAR(200) | Description of the disease.                      |

---

### Table: `DonorDetail`

**Purpose**: Stores blood donor information, including personal and address details.

| Column                | Type        | Description                                        |
| --------------------- | ----------- | -------------------------------------------------- |
| `id`                  | VARCHAR(10) | Primary key, unique identifier (e.g., `DNR001`).   |
| `personal_details_id` | VARCHAR(10) | Foreign key referencing `PersonalDetailsUser(id)`. |
| `address_id`          | VARCHAR(10) | Foreign key referencing `AddressDetailsUser(id)`.  |
| `disease_id`          | VARCHAR(10) | Foreign key referencing `DiseaseDetailsUser(id)`.  |
| `blood_group`         | VARCHAR(10) | Blood group of the donor.                          |
| `last_donated_date`   | DATE        | Date of the last blood donation.                   |
| `active_status`       | BOOLEAN     | Indicates if the donor is actively donating.       |

---

### Table: `AdminDetails`

**Purpose**: Stores details of administrators with access to the system.

| Column              | Type         | Description                                        |
| ------------------- | ------------ | -------------------------------------------------- |
| `id`                | VARCHAR(10)  | Primary key, unique identifier (e.g., `ADM001`).   |
| `username`          | VARCHAR(45)  | Username for admin login.                          |
| `email`             | VARCHAR(100) | Email address of the admin.                        |
| `password`          | VARCHAR(100) | Encrypted password for admin access.               |
| `last_login_date`   | DATETIME     | Last login timestamp.                              |
| `approved_donation` | BOOLEAN      | Indicates if admin has approved donation requests. |

---

### Table: `AuthenticationDetailsAdmin`

**Purpose**: Tracks login details for administrators.

| Column       | Type         | Description                                 |
| ------------ | ------------ | ------------------------------------------- |
| `admin_id`   | VARCHAR(10)  | Foreign key referencing `AdminDetails(id)`. |
| `name`       | VARCHAR(100) | Name of the admin logging in.               |
| `login_date` | DATE         | Date of login.                              |
| `login_time` | TIME         | Time of login.                              |

---

### Table: `HospitalDetails`

**Purpose**: Stores information about hospitals involved in the system.

| Column             | Type         | Description                                       |
| ------------------ | ------------ | ------------------------------------------------- |
| `id`               | VARCHAR(10)  | Primary key, unique identifier (e.g., `HOSP001`). |
| `hospital_name`    | VARCHAR(100) | Name of the hospital.                             |
| `hospital_address` | VARCHAR(200) | Address of the hospital.                          |
| `pincode`          | VARCHAR(10)  | Postal code of the hospital.                      |
| `city`             | VARCHAR(45)  | City where the hospital is located.               |
| `state`            | VARCHAR(45)  | State where the hospital is located.              |
| `country`          | VARCHAR(45)  | Country where the hospital is located.            |
| `branch`           | VARCHAR(45)  | Branch name if applicable.                        |
| `landmark`         | VARCHAR(100) | Nearby landmark if applicable.                    |

---

### Table: `BloodRequestDetails`

**Purpose**: Tracks blood donation requests, including patient details and hospital information.

| Column           | Type         | Description                                      |
| ---------------- | ------------ | ------------------------------------------------ |
| `id`             | VARCHAR(10)  | Primary key, unique identifier (e.g., `REQ001`). |
| `patient_name`   | VARCHAR(100) | Name of the patient in need.                     |
| `blood_group`    | VARCHAR(10)  | Required blood group.                            |
| `hospital_id`    | VARCHAR(10)  | Foreign key referencing `HospitalDetails(id)`.   |
| `contact_number` | VARCHAR(15)  | Contact number for the blood request.            |
| `patient_age`    | INT          | Age of the patient.                              |
| `due_date`       | DATETIME     | Deadline for the blood requirement.              |
| `request_reason` | VARCHAR(200) | Reason for the blood request.                    |
| `status`         | VARCHAR(45)  | Current status of the request (e.g., pending).   |
| `units_required` | INT          | Number of blood units needed.                    |
| `attendant_name` | VARCHAR(100) | Name of the attendant overseeing the patient.    |
| `donor_ids`      | VARCHAR(255) | JSON-like list of donor IDs who have donated.    |
| `response_id`    | VARCHAR(10)  | Foreign key referencing `ResponseDetails(id)`.   |

---

### Table: `ResponseDetails`

**Purpose**: Logs responses to blood donation requests.

| Column             | Type         | Description                                        |
| ------------------ | ------------ | -------------------------------------------------- |
| `id`               | VARCHAR(10)  | Primary key, unique identifier (e.g., `RESP001`).  |
| `blood_request_id` | VARCHAR(10)  | Foreign key referencing `BloodRequestDetails(id)`. |
| `status`           | VARCHAR(45)  | Status of the response (e.g., completed).          |
| `report`           | VARCHAR(255) | Summary report of the donation event.              |
| `units_donated`    | INT          | Number of units donated.                           |
| `donor_ids`        | VARCHAR(255) | JSON-like list of donor IDs who donated.           |

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
