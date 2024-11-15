-- Creating the DonorDetail table
CREATE TABLE DonorDetail (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(500) NOT NULL,
    blood_group VARCHAR(10) NOT NULL,
    personal_details_id VARCHAR(36) NOT NULL,
    address_id VARCHAR(36) NOT NULL,
    active_status BOOLEAN NOT NULL DEFAULT TRUE,
    disease_id VARCHAR(36),
    authentication_id VARCHAR(36) NOT NULL,
    last_donated_date DATETIME,
    number_of_times_donated VARCHAR(36) NOT NULL,
    FOREIGN KEY (personal_details_id) REFERENCES PersonalDetailsUser(id),
    FOREIGN KEY (address_id) REFERENCES AddressDetailsUser(id),
    FOREIGN KEY (disease_id) REFERENCES DiseaseDetailsUser(id),
    FOREIGN KEY (authentication_id) REFERENCES AuthenticationDetailsDonor(id)
);

-- Creating the AuthenticationDetailsDonor table
CREATE TABLE AuthenticationDetailsDonor (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    login_date DATE,
    login_time TIME
);

-- Creating the PersonalDetailsUser table
CREATE TABLE PersonalDetailsUser (
    id VARCHAR(36) PRIMARY KEY,
    first_name VARCHAR(45) NOT NULL,
    last_name VARCHAR(45),
    age INTEGER NOT NULL,
    date_of_birth DATE NOT NULL,
    contact_number VARCHAR(15) NOT NULL,
    secondary_contact_number VARCHAR(15),
    marital_status VARCHAR(10),
    aadhar_number VARCHAR(20)
);

-- Creating the AddressDetailsUser table
CREATE TABLE AddressDetailsUser (
    id VARCHAR(36) PRIMARY KEY,
    address VARCHAR(200) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    country VARCHAR(45) NOT NULL,
    state VARCHAR(45) NOT NULL,
    city VARCHAR(45) NOT NULL
);

-- Creating the DiseaseDetailsUser table
CREATE TABLE DiseaseDetailsUser (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(200)
);

-- Creating the AdminDetails table
CREATE TABLE AdminDetails (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    username VARCHAR(45) NOT NULL,
    authentication_id VARCHAR(36) UNIQUE NOT NULL,
    last_login_date DATETIME,
    approved_donation BOOLEAN NOT NULL DEFAULT FALSE
);

-- Creating the AuthenticationDetailsAdmin table
CREATE TABLE AuthenticationDetailsAdmin (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    auth_id VARCHAR(36) NOT NULL,
    name VARCHAR(100) NOT NULL,
    login_date DATE NOT NULL,
    login_time TIME NOT NULL
);

-- Creating the BloodRequestDetails table
CREATE TABLE BloodRequestDetails (
    id VARCHAR(36) PRIMARY KEY,
    patient_name VARCHAR(100) NOT NULL,
    blood_group VARCHAR(10) NOT NULL,
    hospital_name VARCHAR(100) NOT NULL,
    hospital_id VARCHAR(36) NOT NULL,
    contact_number VARCHAR(15) NOT NULL,
    patient_age INTEGER NOT NULL,
    due_date DATETIME NOT NULL,
    request_reason VARCHAR(200),
    status VARCHAR(45) NOT NULL,
    units_required INTEGER NOT NULL,
    attendant_name VARCHAR(100),
    response_id VARCHAR(36) NOT NULL,
    FOREIGN KEY (hospital_id) REFERENCES HospitalDetails(id),
    FOREIGN KEY (response_id) REFERENCES ResponseDetails(id)
);

-- Creating the HospitalDetails table
CREATE TABLE HospitalDetails (
    id VARCHAR(36) PRIMARY KEY,
    hospital_name VARCHAR(100) NOT NULL,
    hospital_address VARCHAR(200) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    city VARCHAR(45) NOT NULL,
    state VARCHAR(45) NOT NULL,
    country VARCHAR(45) NOT NULL,
    branch VARCHAR(45),
    landmark VARCHAR(100)
);

-- Creating the ResponseDetails table
CREATE TABLE ResponseDetails (
    id VARCHAR(36) PRIMARY KEY,
    status VARCHAR(45),
    report VARCHAR(255),
    units_donated INTEGER,
    donor_ids VARCHAR(255)
);
