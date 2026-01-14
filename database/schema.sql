-- ---------------------------------------------------------
-- 1. ZONAL ORGANIZATION
-- ---------------------------------------------------------
CREATE TABLE zones (
    zone_id INT PRIMARY KEY AUTO_INCREMENT,
    zone_name VARCHAR(255) NOT NULL
);

-- ---------------------------------------------------------
-- 2. USER MANAGEMENT
-- ---------------------------------------------------------
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    otp_code VARCHAR(10),
    user_type VARCHAR(50) NOT NULL, -- 'Donor', 'Volunteer'
    zone_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (zone_id) REFERENCES zones(zone_id)
);

-- ---------------------------------------------------------
-- 3. PROFILES (Donors & Volunteers)
-- ---------------------------------------------------------
CREATE TABLE donors (
    donor_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    business_type VARCHAR(255),
    hygiene_rating INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE volunteers (
    volunteer_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    travel_distance DECIMAL(10, 2),
    green_points INT DEFAULT 0,
    current_lat DECIMAL(10, 8),
    current_long DECIMAL(11, 8),
    referrer_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (referrer_id) REFERENCES volunteers(volunteer_id)
);

-- ---------------------------------------------------------
-- 4. FOOD SURPLUS LISTINGS
-- ---------------------------------------------------------
CREATE TABLE food_listings (
    listing_id INT PRIMARY KEY AUTO_INCREMENT,
    donor_id INT NOT NULL,
    food_details TEXT,
    quantity VARCHAR(255),
    pickup_deadline TIMESTAMP,
    status VARCHAR(50) DEFAULT 'Available', -- 'Available', 'Claimed', 'Delivered', 'Expired'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (donor_id) REFERENCES donors(donor_id)
);

-- ---------------------------------------------------------
-- 5. DELIVERY LOGISTICS
-- ---------------------------------------------------------
CREATE TABLE deliveries (
    delivery_id INT PRIMARY KEY AUTO_INCREMENT,
    listing_id INT NOT NULL,
    volunteer_id INT NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    FOREIGN KEY (listing_id) REFERENCES food_listings(listing_id),
    FOREIGN KEY (volunteer_id) REFERENCES volunteers(volunteer_id)
);

-- ---------------------------------------------------------
-- 6. FINANCE & GAMIFICATION
-- ---------------------------------------------------------
CREATE TABLE logistics_fund (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    delivery_id INT NOT NULL,
    sponsor_name VARCHAR(255),
    amount DECIMAL(10, 2),
    status VARCHAR(50),
    FOREIGN KEY (delivery_id) REFERENCES deliveries(delivery_id)
);

CREATE TABLE points_history (
    point_id INT PRIMARY KEY AUTO_INCREMENT,
    volunteer_id INT NOT NULL,
    point_type VARCHAR(50), -- 'Delivery', 'Referral'
    amount INT,
    awarded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (volunteer_id) REFERENCES volunteers(volunteer_id)
);

-- ---------------------------------------------------------
-- 7. FEEDBACK & MESSAGING
-- ---------------------------------------------------------
CREATE TABLE reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    delivery_id INT NOT NULL,
    reviewer_id INT NOT NULL,
    subject_id INT NOT NULL,
    rating INT,
    comment TEXT,
    FOREIGN KEY (delivery_id) REFERENCES deliveries(delivery_id),
    FOREIGN KEY (reviewer_id) REFERENCES users(user_id),
    FOREIGN KEY (subject_id) REFERENCES users(user_id)
);

CREATE TABLE messages (
    message_id INT PRIMARY KEY AUTO_INCREMENT,
    delivery_id INT NOT NULL,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    content TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (delivery_id) REFERENCES deliveries(delivery_id),
    FOREIGN KEY (sender_id) REFERENCES users(user_id),
    FOREIGN KEY (receiver_id) REFERENCES users(user_id)
);