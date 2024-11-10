-- Database creation
CREATE DATABASE IF NOT EXISTS YouthRedCross_BloodRequest;
USE YouthRedCross_BloodRequest;

-- Table: PersonalDetailsUser
CREATE TABLE PersonalDetailsUser (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(45) NOT NULL,
    last_name VARCHAR(45),
    age INT NOT NULL,
    date_of_birth DATE NOT NULL,
    contact_number VARCHAR(15) NOT NULL,
    secondary_contact_number VARCHAR(15),
    marital_status VARCHAR(10),
    aadhar_number VARCHAR(20)
);

-- Table: AddressDetailsUser
CREATE TABLE AddressDetailsUser (
    id INT PRIMARY KEY AUTO_INCREMENT,
    address VARCHAR(200) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    country VARCHAR(45) NOT NULL,
    state VARCHAR(45) NOT NULL,
    city VARCHAR(45) NOT NULL
);

-- Table: DiseaseDetailsUser
CREATE TABLE DiseaseDetailsUser (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(200)
);

-- Table: DonorDetail
CREATE TABLE DonorDetail (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    blood_group VARCHAR(10) NOT NULL,
    personal_details_id INT NOT NULL,
    address_id INT NOT NULL,
    active_status BOOLEAN NOT NULL DEFAULT TRUE,
    disease_id INT,
    last_donated_date DATETIME,
    FOREIGN KEY (personal_details_id) REFERENCES PersonalDetailsUser(id),
    FOREIGN KEY (address_id) REFERENCES AddressDetailsUser(id),
    FOREIGN KEY (disease_id) REFERENCES DiseaseDetailsUser(id)
);

-- Table: AdminDetails
CREATE TABLE AdminDetails (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    username VARCHAR(45) NOT NULL,
    last_login_date DATETIME,
    approved_donation BOOLEAN NOT NULL DEFAULT FALSE
);

-- Table: AuthenticationDetailsAdmin
CREATE TABLE AuthenticationDetailsAdmin (
    admin_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    login_date DATE NOT NULL,
    login_time TIME NOT NULL,
    FOREIGN KEY (admin_id) REFERENCES AdminDetails(id)
);

-- Table: HospitalDetails
CREATE TABLE HospitalDetails (
    id INT PRIMARY KEY AUTO_INCREMENT,
    hospital_name VARCHAR(100) NOT NULL,
    hospital_address VARCHAR(200) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    city VARCHAR(45) NOT NULL,
    state VARCHAR(45) NOT NULL,
    country VARCHAR(45) NOT NULL,
    branch VARCHAR(45),
    landmark VARCHAR(100)
);

-- Table: BloodRequestDetails
CREATE TABLE BloodRequestDetails (
    id INT PRIMARY KEY AUTO_INCREMENT,
    patient_name VARCHAR(100) NOT NULL,
    blood_group VARCHAR(10) NOT NULL,
    hospital_name VARCHAR(100) NOT NULL,
    hospital_id INT NOT NULL,
    contact_number VARCHAR(15) NOT NULL,
    patient_age INT NOT NULL,
    due_date DATETIME NOT NULL,
    request_reason VARCHAR(200),
    status VARCHAR(45) NOT NULL,
    units_required INT NOT NULL,
    attendant_name VARCHAR(100),
    donor_ids VARCHAR(255),
    response_id INT,
    FOREIGN KEY (hospital_id) REFERENCES HospitalDetails(id),
    FOREIGN KEY (response_id) REFERENCES ResponseDetails(id)
);

-- Table: ResponseDetails
CREATE TABLE ResponseDetails (
    id INT PRIMARY KEY AUTO_INCREMENT,
    blood_request_id INT NOT NULL,
    status VARCHAR(45) NOT NULL,
    report VARCHAR(255),
    units_donated INT NOT NULL,
    donor_ids VARCHAR(255),
    FOREIGN KEY (blood_request_id) REFERENCES BloodRequestDetails(id)
);
