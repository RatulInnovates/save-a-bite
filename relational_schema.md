# Relational Database Schema: SaveABite

## Tables and Fields
* [cite_start]**zones:** `zone_id` (PK), `zone_name`[cite: 1, 5, 14].
* [cite_start]**users:** `user_id` (PK), `name`, `email`, `password_hash`, `otp_code`, `user_type`, `zone_id` (FK)[cite: 2, 7, 24, 30, 37, 39, 41, 15].
* [cite_start]**donors:** `donor_id` (PK), `user_id` (FK), `business_type`, `hygiene_rating`[cite: 3, 9, 32, 26].
* [cite_start]**volunteers:** `volunteer_id` (PK), `user_id` (FK), `travel_distance`, `green_points`, `current_lat`, `current_long`, `referrer_id` (FK)[cite: 55, 62, 66, 64, 71, 73, 74, 69].
* [cite_start]**food_listings:** `listing_id` (PK), `donor_id` (FK), `food_details`, `quantity`, `pickup_deadline`, `status`, `created_at`[cite: 4, 12, 19, 27, 36, 50, 43, 22].
* [cite_start]**deliveries:** `delivery_id` (PK), `listing_id` (FK), `volunteer_id` (FK), `status`, `start_time`, `end_time`[cite: 11, 20, 28, 34, 92, 44, 58].
* [cite_start]**logistics_fund:** `transaction_id` (PK), `delivery_id` (FK), `sponsor_name`, `amount`[cite: 70, 87, 85, 90].
* [cite_start]**points_history:** `point_id` (PK), `volunteer_id` (FK), `point_type`, `amount`, `awarded_at`[cite: 76, 77, 78, 79, 80, 81].
* **reviews:** `review_id` (PK), `delivery_id` (FK), `reviewer_id` (FK), `subject_id` (FK), `rating`, `comment`[cite: 94, 95, 97, 99, 101, 103, 105].
* [cite_start]**messages:** `message_id` (PK), `delivery_id` (FK), `sender_id` (FK), `receiver_id` (FK), `content`, `sent_at`[cite: 106, 107, 108, 111, 113, 115, 117].

## Key Relationships
1. [cite_start]**Zonal Logic:** `users` and `food_listings` are tied to `zones` for hyper-local matching[cite: 138, 150].
2. [cite_start]**Verification:** `donors` and `volunteers` interact through `deliveries` using `otp_code` for validation[cite: 143, 146].
3. [cite_start]**Safety:** `hygiene_rating` in `donors` and `pickup_deadline` in `food_listings` ensure food safety[cite: 124, 132].s