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

-- Insert disease details with unique IDs for each donor
INSERT INTO DiseaseDetailsUser (id, name, description) VALUES
('DIS001', 'Diabetes', 'A disease that occurs when your blood glucose is too high.'),
('DIS002', 'Hypertension', 'A condition in which the blood vessels have persistently raised pressure.'),
('DIS003', 'Diabetes', 'A disease that occurs when your blood glucose is too high.'),
('DIS004', 'Asthma', 'A respiratory condition that causes difficulty in breathing.'),
('DIS005', 'Hypertension', 'A condition in which the blood vessels have persistently raised pressure.'),
('DIS006', 'Heart Disease', 'A range of conditions affecting the heart.'),
('DIS007', 'Anemia', 'A condition marked by a deficiency of red blood cells.'),
('DIS008', 'Diabetes', 'A disease that occurs when your blood glucose is too high.'),
('DIS009', 'Hypertension', 'A condition in which the blood vessels have persistently raised pressure.'),
('DIS010', 'Asthma', 'A respiratory condition that causes difficulty in breathing.');

-- Inserting into AuthenticationDetailsAdmin
INSERT INTO AuthenticationDetailsAdmin (id, auth_id, name, login_date, login_time) VALUES
(1,'AUTHADM001', 'Admin One', '2024-01-01', '09:00:00');

-- Inserting into AdminDetails
INSERT INTO AdminDetails (id, email, password, username, authentication_id, vec_registration_number, data_of_birth , mobile_number , department , active_status ,last_login_date, approved_donation) VALUES
('ADMIN001', 'siddharthmagesh007@gmail.com', 'scrypt:32768:8:1$XIjoEBWPpgO1inbw$9fbef6e94d1d9d11c3763df2337ed22f17a478b4fb37ce45d7e227c084a2b77ccf4f21079b963bf88ac5a6f31ba4042de48cff5f9c5c0e27de0b811e7c55cc78', 'Siddharth Magesh', 'AUTHADM001', '113222072xxx', '2004-03-22' ,'9876543210' , 'AIDS', 'Active' ,'2024-01-01', 2),
('ADMIN002', 'siddha2234@gmail.com', 'scrypt:32768:8:1$O1tTJmR4WSfVwesv$16f2e93c67d374cf3a4cb2f127accac6ffb3cf079748a77e4383cf1b5dd71d6d3b475a85df459ba314101004bf10072811b83ea85dbb4420e4ad11f1a873875e', 'Admin 2', 'AUTHADM002', '113222072xxy', '2004-03-22' ,'9876543210' , 'AIDS', 'Active' ,'2024-01-01', 0);

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
INSERT INTO ResponseDetails (id, status, report, units_donated, certificate_status, donor_ids) VALUES
('RESP001', 'Success', 'Blood successfully donated', 2, 'SENT' ,'DNR001,DNR002'),
('RESP002', NULL, NULL, 0,'NOTSENT',NULL),
('RESP003', NULL, NULL, 0,'NOTSENT',NULL),
('RESP004', NULL, NULL, 0,'NOTSENT',NULL);

-- Inserting into BloodRequestDetails
INSERT INTO BloodRequestDetails (id, patient_name, blood_group, hospital_name, hospital_id, contact_number, patient_age, due_date, request_reason, status, units_required, attendant_name, response_id) VALUES
('BR001', 'John Smith', 'O+', 'Apollo Hospital', 'HOSP001', '1234567890', 30, '2024-02-15', 'Surgery', 'Closed', 2, 'Attendant One', 'RESP001'),
('BR002', 'Jane Doe', 'A-', 'Fortis Malar Hospital', 'HOSP002', '2345678901', 25, '2024-03-10', 'Emergency', 'Not_Approved', 1, 'Attendant Two', 'RESP002'),
('BR003', 'Jane Doe 1', 'A-', 'MIOT International', 'HOSP004', '2345678922', 25, '2024-03-10', 'Emergency', 'Expired', 1, 'Attendant Three', 'RESP003'),
('BR004', 'Jane Doe 2', 'AB-', 'Vijaya Hospital', 'HOSP007', '2345678434', 25, '2024-03-10', 'Emergency', 'Pending', 1, 'Attendant Four', 'RESP004');


INSERT INTO AuthenticationDetailsDonor (id, auth_id ,name, login_date, login_time) VALUES
(1 , 'AUTHDNR001', 'John Doe', '2024-01-01', '09:00:00');


-- Insert donor details with unique disease IDs for each donor
INSERT INTO DonorDetail (id, name, email, password, blood_group, personal_details_id, address_id, active_status, disease_id, authentication_id, last_donated_date, number_of_times_donated, last_login_date) VALUES
('DNR001', 'John Doe', 'john.doe@example.com', 'scrypt:32768:8:1$XIjoEBWPpgO1inbw$9fbef6e94d1d9d11c3763df2337ed22f17a478b4fb37ce45d7e227c084a2b77ccf4f21079b963bf88ac5a6f31ba4042de48cff5f9c5c0e27de0b811e7c55cc78', 'O+', 'PDDNR001', 'ADDR001', TRUE, 'DIS001', 'AUTHDNR001', '2023-01-15', 0, NULL),
('DNR002', 'Jane Smith', 'siddha2234@gmail.com', 'scrypt:32768:8:1$XIjoEBWPpgO1inbw$9fbef6e94d1d9d11c3763df2337ed22f17a478b4fb37ce45d7e227c084a2b77ccf4f21079b963bf88ac5a6f31ba4042de48cff5f9c5c0e27de0b811e7c55cc78', 'A-', 'PDDNR002', 'ADDR002', TRUE, 'DIS002', 'AUTHDNR002', '2023-05-20', 2, NULL),
('DNR003', 'Alice Johnson', 'alice.johnson@example.com', 'password123', 'B+', 'PDDNR003', 'ADDR003', TRUE, 'DIS003', 'AUTHDNR003', '2023-03-10', 0, NULL),
('DNR004', 'Bob Williams', 'bob.williams@example.com', 'password123', 'AB-', 'PDDNR004', 'ADDR004', TRUE, 'DIS004', 'AUTHDNR004', '2023-07-20', 0, NULL),
('DNR005', 'Charlie Brown', 'charlie.brown@example.com', 'password123', 'O-', 'PDDNR005', 'ADDR005', FALSE, 'DIS005', 'AUTHDNR005', '2023-11-30', 0, NULL),
('DNR006', 'Emily Davis', 'emily.davis@example.com', 'password123', 'A+', 'PDDNR006', 'ADDR006', TRUE, 'DIS006', 'AUTHDNR006', '2023-05-21', 0, NULL),
('DNR007', 'Michael Miller', 'michael.miller@example.com', 'password123', 'B-', 'PDDNR007', 'ADDR007', TRUE, 'DIS007', 'AUTHDNR007', '2023-09-15', 0, NULL),
('DNR008', 'Sarah Garcia', 'sarah.garcia@example.com', 'password123', 'O+', 'PDDNR008', 'ADDR008', FALSE, 'DIS008', 'AUTHDNR008', '2023-04-28', 2, NULL),
('DNR009', 'David Rodriguez', '22f3002579@ds.study.iitm.ac.in', 'password123', 'A-', 'PDDNR009', 'ADDR009', TRUE, 'DIS009', 'AUTHDNR009', '2023-08-19', 0, NULL),
('DNR010', 'Siddharth Magesh', 'siddharthmagesh007@gmail.com', 'password123', 'AB+', 'PDDNR010', 'ADDR010', TRUE, 'DIS010', 'AUTHDNR010', '2023-01-15', 0, NULL);

