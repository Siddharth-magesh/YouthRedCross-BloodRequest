# Database Structure Documentation

## Tables

### DonorDetail

| Column                    | Data Type    | Constraints                                 | Description                               |
| ------------------------- | ------------ | ------------------------------------------- | ----------------------------------------- |
| `id`                      | VARCHAR(36)  | PRIMARY KEY                                 | Unique identifier for each donor          |
| `name`                    | VARCHAR(100) | NOT NULL                                    | Name of the donor                         |
| `email`                   | VARCHAR(100) | UNIQUE, NOT NULL                            | Email address of the donor                |
| `password`                | VARCHAR(500) | NOT NULL                                    | Password for the donor's account (hashed) |
| `blood_group`             | VARCHAR(10)  | NOT NULL                                    | Blood group of the donor                  |
| `personal_details_id`     | VARCHAR(36)  | FOREIGN KEY (PersonalDetailsUser.id)        | Links to donor's personal details         |
| `address_id`              | VARCHAR(36)  | FOREIGN KEY (AddressDetailsUser.id)         | Links to donor's address details          |
| `active_status`           | BOOLEAN      | NOT NULL, DEFAULT TRUE                      | Indicates if donor is active              |
| `disease_id`              | VARCHAR(36)  | FOREIGN KEY (DiseaseDetailsUser.id)         | Links to donor's disease details          |
| `authentication_id`       | VARCHAR(36)  | FOREIGN KEY (AuthenticationDetailsDonor.id) | Links to donor's authentication details   |
| `last_donated_date`       | DATETIME     |                                             | Last donation date                        |
| `number_of_times_donated` | VARCHAR(36)  | NOT NULL                                    | Number of times the donor has donated     |

### AuthenticationDetailsDonor

| Column       | Data Type    | Constraints | Description       |
| ------------ | ------------ | ----------- | ----------------- |
| `id`         | VARCHAR(36)  | PRIMARY KEY | Unique identifier |
| `name`       | VARCHAR(100) | NOT NULL    | Name of the donor |
| `login_date` | DATE         |             | Last login date   |
| `login_time` | TIME         |             | Last login time   |

### PersonalDetailsUser

| Column                     | Data Type   | Constraints | Description              |
| -------------------------- | ----------- | ----------- | ------------------------ |
| `id`                       | VARCHAR(36) | PRIMARY KEY | Unique identifier        |
| `first_name`               | VARCHAR(45) | NOT NULL    | First name               |
| `last_name`                | VARCHAR(45) |             | Last name                |
| `age`                      | INTEGER     | NOT NULL    | Age of the donor         |
| `date_of_birth`            | DATE        | NOT NULL    | Date of birth            |
| `contact_number`           | VARCHAR(15) | NOT NULL    | Primary contact number   |
| `secondary_contact_number` | VARCHAR(15) |             | Secondary contact number |
| `marital_status`           | VARCHAR(10) |             | Marital status           |
| `aadhar_number`            | VARCHAR(20) |             | Aadhaar number           |

### AddressDetailsUser

| Column    | Data Type    | Constraints | Description       |
| --------- | ------------ | ----------- | ----------------- |
| `id`      | VARCHAR(36)  | PRIMARY KEY | Unique identifier |
| `address` | VARCHAR(200) | NOT NULL    | Address line      |
| `pincode` | VARCHAR(10)  | NOT NULL    | Pincode           |
| `country` | VARCHAR(45)  | NOT NULL    | Country           |
| `state`   | VARCHAR(45)  | NOT NULL    | State             |
| `city`    | VARCHAR(45)  | NOT NULL    | City              |

### DiseaseDetailsUser

| Column        | Data Type    | Constraints | Description         |
| ------------- | ------------ | ----------- | ------------------- |
| `id`          | VARCHAR(36)  | PRIMARY KEY | Unique identifier   |
| `name`        | VARCHAR(100) | NOT NULL    | Name of the disease |
| `description` | VARCHAR(200) |             | Disease description |

### AdminDetails

| Column              | Data Type    | Constraints             | Description                             |
| ------------------- | ------------ | ----------------------- | --------------------------------------- |
| `id`                | VARCHAR(36)  | PRIMARY KEY             | Unique identifier                       |
| `email`             | VARCHAR(100) | UNIQUE, NOT NULL        | Email of the admin                      |
| `password`          | VARCHAR(100) | NOT NULL                | Admin's password (hashed)               |
| `username`          | VARCHAR(45)  | NOT NULL                | Admin username                          |
| `authentication_id` | VARCHAR(36)  | UNIQUE, NOT NULL        | Links to admin's authentication details |
| `last_login_date`   | DATETIME     |                         | Last login date                         |
| `approved_donation` | BOOLEAN      | NOT NULL, DEFAULT FALSE | Indicates if admin approved donation    |

### AuthenticationDetailsAdmin

| Column       | Data Type    | Constraints                | Description                 |
| ------------ | ------------ | -------------------------- | --------------------------- |
| `id`         | INTEGER      | PRIMARY KEY AUTO_INCREMENT | Auto-incrementing unique ID |
| `auth_id`    | VARCHAR(36)  | NOT NULL                   | Unique authentication ID    |
| `name`       | VARCHAR(100) | NOT NULL                   | Admin's name                |
| `login_date` | DATE         | NOT NULL                   | Login date                  |
| `login_time` | TIME         | NOT NULL                   | Login time                  |

### BloodRequestDetails

| Column           | Data Type    | Constraints                      | Description                |
| ---------------- | ------------ | -------------------------------- | -------------------------- |
| `id`             | VARCHAR(36)  | PRIMARY KEY                      | Unique identifier          |
| `patient_name`   | VARCHAR(100) | NOT NULL                         | Name of the patient        |
| `blood_group`    | VARCHAR(10)  | NOT NULL                         | Blood group needed         |
| `hospital_name`  | VARCHAR(100) | NOT NULL                         | Name of the hospital       |
| `hospital_id`    | VARCHAR(36)  | FOREIGN KEY (HospitalDetails.id) | Links to hospital details  |
| `contact_number` | VARCHAR(15)  | NOT NULL                         | Contact number             |
| `patient_age`    | INTEGER      | NOT NULL                         | Age of the patient         |
| `due_date`       | DATETIME     | NOT NULL                         | Due date for blood request |
| `request_reason` | VARCHAR(200) |                                  | Reason for request         |
| `status`         | VARCHAR(45)  | NOT NULL                         | Request status             |
| `units_required` | INTEGER      | NOT NULL                         | Number of units required   |
| `attendant_name` | VARCHAR(100) |                                  | Name of the attendant      |
| `response_id`    | VARCHAR(36)  | FOREIGN KEY (ResponseDetails.id) | Links to response details  |

### HospitalDetails

| Column             | Data Type    | Constraints | Description                        |
| ------------------ | ------------ | ----------- | ---------------------------------- |
| `id`               | VARCHAR(36)  | PRIMARY KEY | Unique identifier                  |
| `hospital_name`    | VARCHAR(100) | NOT NULL    | Name of the hospital               |
| `hospital_address` | VARCHAR(200) | NOT NULL    | Address of the hospital            |
| `pincode`          | VARCHAR(10)  | NOT NULL    | Pincode of the hospital            |
| `city`             | VARCHAR(45)  | NOT NULL    | City where the hospital is located |
| `state`            | VARCHAR(45)  | NOT NULL    | State                              |
| `country`          | VARCHAR(45)  | NOT NULL    | Country                            |
| `branch`           | VARCHAR(45)  |             | Branch (if applicable)             |
| `landmark`         | VARCHAR(100) |             | Landmark nearby                    |

### ResponseDetails

| Column          | Data Type    | Constraints | Description                   |
| --------------- | ------------ | ----------- | ----------------------------- |
| `id`            | VARCHAR(36)  | PRIMARY KEY | Unique identifier             |
| `status`        | VARCHAR(45)  |             | Response status               |
| `report`        | VARCHAR(255) |             | Report details                |
| `units_donated` | INTEGER      |             | Number of units donated       |
| `donor_ids`     | VARCHAR(255) |             | IDs of donors who contributed |

---

## Relationships

1. **DonorDetail Table**:

   - `personal_details_id` references `PersonalDetailsUser.id`.
   - `address_id` references `AddressDetailsUser.id`.
   - `disease_id` references `DiseaseDetailsUser.id`.
   - `authentication_id` references `AuthenticationDetailsDonor.id`.

2. **BloodRequestDetails Table**:
   - `hospital_id` references `HospitalDetails.id`.
   - `response_id` references `ResponseDetails.id`.

Each table's foreign key links back to a unique identifier in the corresponding table, ensuring relational integrity across donor details, hospital details, and response tracking.
