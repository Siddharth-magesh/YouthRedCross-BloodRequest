use main;

-- Inserting into AdminDetails
INSERT INTO AdminDetails (id, email, password, username, authentication_id, vec_registration_number, data_of_birth , mobile_number , department , active_status ,last_login_date, approved_donation_count,closed_requests_count) VALUES
('ADMIN001', 'siddharthmagesh007@gmail.com', 'scrypt:32768:8:1$XIjoEBWPpgO1inbw$9fbef6e94d1d9d11c3763df2337ed22f17a478b4fb37ce45d7e227c084a2b77ccf4f21079b963bf88ac5a6f31ba4042de48cff5f9c5c0e27de0b811e7c55cc78', 'Siddharth Magesh', 'AUTHADM001', '113222072094', '2004-03-22' ,'9150450401' , 'AIDS', 'Active' ,'2024-01-01', 2,0);