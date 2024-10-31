use test1;

-- Inserting into PersonalDetailsUser
INSERT INTO PersonalDetailsUser (id, first_name, last_name, age, date_of_birth, contact_number, secondary_contact_number, marital_status, aadhar_number) VALUES
('PDDNR001', 'John', 'Doe', 30, '1994-05-12', '1234567890', '0987654321', 'Single', '1234-5678-9101'),
('PDDNR002', 'Jane', 'Smith', 28, '1996-02-15', '2345678901', NULL, 'Married', '2345-6789-0123'),
('PDDNR003', 'Alice', 'Johnson', 35, '1988-03-10', '3456789012', '1234567891', 'Single', '3456-7890-1234'),
('PDDNR004', 'Bob', 'Williams', 40, '1983-07-20', '4567890123', NULL, 'Divorced', '4567-8901-2345'),
('PDDNR005', 'Charlie', 'Brown', 32, '1991-11-30', '5678901234', '6789012345', 'Married', '5678-9012-3456'),
('PDDNR006', 'Emily', 'Davis', 29, '1995-05-21', '6789012345', '7890123456', 'Single', '6789-0123-4567'),
('PDDNR007', 'Michael', 'Miller', 37, '1986-09-15', '7890123456', NULL, 'Married', '7890-1234-5678'),
('PDDNR008', 'Sarah', 'Garcia', 26, '1997-04-28', '8901234567', '9012345678', 'Single', '8901-2345-6789'),
('PDDNR009', 'David', 'Rodriguez', 31, '1992-08-19', '9012345678', NULL, 'Married', '9012-3456-7890'),
('PDDNR010', 'Siddharth', 'Magesh', 27, '1996-01-15', '0123456789', '1234567890', 'Single', '0123-4567-8901');

-- Inserting into AddressDetailsUser
INSERT INTO AddressDetailsUser (id, address, pincode, country, state, city) VALUES
('ADDR001', '63, villivakkam road, Lakshmipuram , kolathur ,Chennai', '600001', 'India', 'Tamil Nadu', 'Chennai'),
('ADDR002', 'No:57/7, Subash nagar 1st street,Puthagaram, Kolathur', '600002', 'India', 'Tamil Nadu', 'Chennai'),
('ADDR003', 'No 11 periyar main street srinivasa nagar padi Chennai 50', '600003', 'India', 'Tamil Nadu', 'Chennai'),
('ADDR004', 'No. 15 , Mani street, Vijayalakshmi puram, Ambattur, Chennai', '600004', 'India', 'Tamil Nadu', 'Chennai'),
('ADDR005', 'No5 Jothiramalingam street kannigapuram Avadi Chennai 54', '600005', 'India', 'Tamil Nadu', 'Chennai'),
('ADDR006', 'Ng3, Hansa Garden, Madambakkam Main Road, Rajakilpakkam', '600006', 'India', 'Tamil Nadu', 'Chennai'),
('ADDR007', 'No 44 kannikapuram Gandhi street Avadi Chennai 54', '600007', 'India', 'Tamil Nadu', 'Chennai'),
('ADDR008', 'No : 50 Church Street Venkateshwara Nagar entn Ambattur Chennai 53 ', '600008', 'India', 'Tamil Nadu', 'Chennai'),
('ADDR009', '1/232B, Omakulam Street, Shakthi Nagar, Periya Mathur, Chennai - 600068', '600009', 'India', 'Tamil Nadu', 'Chennai'),
('ADDR010', 'No:5/289,burnar salai,mogappair east, chennai-37.', '600010', 'India', 'Tamil Nadu', 'Chennai');

-- Inserting into DiseaseDetailsUser
INSERT INTO DiseaseDetailsUser (id, name, description) VALUES
('DIS001', 'Diabetes', 'A disease that occurs when your blood glucose is too high.'),
('DIS002', 'Hypertension', 'A condition in which the blood vessels have persistently raised pressure.');

-- Inserting into AuthenticationDetailsAdmin
INSERT INTO AuthenticationDetailsAdmin (id, auth_id, name, login_date, login_time) VALUES
(1,'AUTHADM001', 'Admin One', '2024-01-01', '09:00:00'),
(2,'AUTHADM002', 'Admin Two', '2024-01-02', '10:00:00');

-- Inserting into AdminDetails
INSERT INTO AdminDetails (id, email, password, username, authentication_id, last_login_date, approved_donation) VALUES
('ADMIN001', 'admin1@example.com', 'password1', 'admin1', 'AUTHADM001', '2024-01-01', FALSE),
('ADMIN002', 'admin2@example.com', 'password2', 'admin2', 'AUTHADM002', '2024-01-02', TRUE);

-- Inserting into HospitalDetails
INSERT INTO HospitalDetails (id, hospital_name, hospital_address, pincode, city, state, country, branch, landmark) VALUES
('HOSP001', 'Apollo Hospital', 'No. 21, Greams Lane, Off Greams Road', '600006', 'Chennai', 'Tamil Nadu', 'India', 'Main', 'Near Greams Road'),
('HOSP002', 'Fortis Malar Hospital', 'No. 52, 1st Main Road, Gandhi Nagar, Adyar', '600020', 'Chennai', 'Tamil Nadu', 'India', 'Branch', 'Near Adyar Signal'),
('HOSP003', 'Billroth Hospital', 'No. 43, B, P. V. B. Road, Shenoy Nagar', '600030', 'Chennai', 'Tamil Nadu', 'India', 'Main', 'Near Shenoy Nagar Metro Station'),
('HOSP004', 'MIOT International', 'No. 4, Mount Road, Manapakkam', '600116', 'Chennai', 'Tamil Nadu', 'India', 'Branch', 'Near Mount Road Junction'),
('HOSP005', 'Sri Ramachandra Medical Center', 'No. 1, Ramachandra Nagar, Porur', '600116', 'Chennai', 'Tamil Nadu', 'India', 'Main', 'Near Porur Junction'),
('HOSP006', 'KMC Hospital', 'No. 1, Kotturpuram', '600085', 'Chennai', 'Tamil Nadu', 'India', 'Branch', 'Near Kotturpuram Bridge'),
('HOSP007', 'Vijaya Hospital', 'No. 50, Kottur Garden', '600085', 'Chennai', 'Tamil Nadu', 'India', 'Main', 'Near Kottur Garden Park'),
('HOSP008', 'Gleneagles Global Health City', 'No. 2, 1st Floor, East Coast Road', '600041', 'Chennai', 'Tamil Nadu', 'India', 'Branch', 'Near ECR Road'),
('HOSP009', 'Sundaram Medical Foundation', 'No. 2, Padmavathy Nagar, Ayanambakkam', '600095', 'Chennai', 'Tamil Nadu', 'India', 'Main', 'Near Ayanambakkam Bus Stop'),
('HOSP010', 'Sakthi Hospital', 'No. 14, K.K. Nagar', '600078', 'Chennai', 'Tamil Nadu', 'India', 'Branch', 'Near K.K. Nagar');

-- Inserting into ResponseDetails
INSERT INTO ResponseDetails (id, status, report, units_donated, donor_ids) VALUES
('RESP001', 'Success', 'Blood successfully donated', 2, 'DNR001,DNR002'),
('RESP002', NULL, NULL, 0, NULL),
('RESP003', NULL, NULL, 0, NULL),
('RESP004', NULL, NULL, 0, NULL);

-- Inserting into BloodRequestDetails
INSERT INTO BloodRequestDetails (id, patient_name, blood_group, hospital_name, hospital_id, contact_number, patient_age, due_date, request_reason, status, units_required, attendant_name, response_id) VALUES
('BR001', 'John Smith', 'O+', 'General Hospital', 'HOSP001', '1234567890', 30, '2024-02-15', 'Surgery', 'Closed', 2, 'Attendant One', 'RESP001'),
('BR002', 'Jane Doe', 'A-', 'City Hospital', 'HOSP002', '2345678901', 25, '2024-03-10', 'Emergency', 'Not_Approved', 1, 'Attendant Two', 'RESP002'),
('BR003', 'Jane Doe 1', 'A-', 'City Hospital', 'HOSP004', '2345678922', 25, '2024-03-10', 'Emergency', 'Expired', 1, 'Attendant Three', 'RESP003'),
('BR004', 'Jane Doe 2', 'AB-', 'City Hospital', 'HOSP007', '2345678434', 25, '2024-03-10', 'Emergency', 'Pending', 1, 'Attendant Four', 'RESP004');


INSERT INTO AuthenticationDetailsDonor (id, name, login_date, login_time) VALUES
('AUTHDNR001', 'John Doe', '2024-01-01', '09:00:00'),
('AUTHDNR002', 'Jane Smith', '2024-01-02', '10:00:00'),
('AUTHDNR003', 'Alice Johnson', '2024-01-03', '11:00:00'),
('AUTHDNR004', 'Bob Williams', '2024-01-04', '12:00:00'),
('AUTHDNR005', 'Charlie Brown', '2024-01-05', '13:00:00'),
('AUTHDNR006', 'Emily Davis', '2024-01-06', '14:00:00'),
('AUTHDNR007', 'Michael Miller', '2024-01-07', '15:00:00'),
('AUTHDNR008', 'Sarah Garcia', '2024-01-08', '16:00:00'),
('AUTHDNR009', 'David Rodriguez', '2024-01-09', '17:00:00'),
('AUTHDNR010', 'Sophia Martinez', '2024-01-10', '18:00:00');

-- Inserting into DonorDetail
INSERT INTO DonorDetail (id, name, email, password, blood_group, personal_details_id, address_id, active_status, disease_id, authentication_id, last_donated_date,number_of_times_donated) VALUES
('DNR001', 'John Doe', 'john.doe@example.com', 'password123', 'O+', 'PDDNR001', 'ADDR001', TRUE, 'DIS001', 'AUTHDNR001', '2023-01-15',0),
('DNR002', 'Jane Smith', 'siddha2234@gmail.com', 'password123', 'A-', 'PDDNR002', 'ADDR002', TRUE, NULL, 'AUTHDNR002', '2023-05-20',2),
('DNR003', 'Alice Johnson', 'alice.johnson@example.com', 'password123', 'B+', 'PDDNR003', 'ADDR003', TRUE, 'DIS002', 'AUTHDNR003', '2023-03-10',0),
('DNR004', 'Bob Williams', 'bob.williams@example.com', 'password123', 'AB-', 'PDDNR004', 'ADDR004', TRUE, NULL, 'AUTHDNR004', '2023-07-20',0),
('DNR005', 'Charlie Brown', 'charlie.brown@example.com', 'password123', 'O-', 'PDDNR005', 'ADDR005', TRUE, 'DIS001', 'AUTHDNR005', '2023-11-30',0),
('DNR006', 'Emily Davis', 'emily.davis@example.com', 'password123', 'A+', 'PDDNR006', 'ADDR006', TRUE, NULL, 'AUTHDNR006', '2023-05-21',0),
('DNR007', 'Michael Miller', 'michael.miller@example.com', 'password123', 'B-', 'PDDNR007', 'ADDR007', TRUE, 'DIS002', 'AUTHDNR007', '2023-09-15',0),
('DNR008', 'Sarah Garcia', 'sarah.garcia@example.com', 'password123', 'O+', 'PDDNR008', 'ADDR008', TRUE, NULL, 'AUTHDNR008', '2023-04-28',2),
('DNR009', 'David Rodriguez', '22f3002579@ds.study.iitm.ac.in', 'password123', 'A-', 'PDDNR009', 'ADDR009', TRUE, 'DIS001', 'AUTHDNR009', '2023-08-19',0),
('DNR010', 'Siddharth Magesh', 'siddharthmagesh007@gmail.com', 'password123', 'AB+', 'PDDNR010', 'ADDR010', TRUE, NULL, 'AUTHDNR010', '2023-01-15',0);

