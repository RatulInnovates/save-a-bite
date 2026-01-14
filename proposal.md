# Project Proposal: SaveABite

## 1. Project Overview
SaveABite is a hyper-local web-based marketplace designed to bridge the logistical gap between food surplus and food insecurity in Bangladesh. It connects food donors (restaurants, convention centers) with distribution units (NGOs, Volunteers).

## 2. Core Logic & Features
* **Automated Volunteer Matching:** Uses stored procedures to match a Food_Listing with the nearest Volunteer based on location.
* **Real-Time Expiry Engine:** A MySQL Event Scheduler runs every 15 minutes to update listing status to 'Expired' if the pickup time has passed.
* **Gamification:** Database Triggers award "Green Points" to volunteers upon successful delivery validation via OTP scan.
* **Dual-Layer Verification:** Volunteers rate Donor hygiene, and Donors verify Volunteer arrival via OTP.
* **Monetary Logistics Fund:** ACID Transactions manage a fund for public sponsorship of volunteer ride costs (e.g., rickshaw fare).
* **Zonal Leaderboards:** Uses SQL Window Functions (`DENSE_RANK()`) to rank volunteers by zone.
* **Waste Trend Analytics:** Uses complex aggregation and `LAG()` functions to compare donor waste week-over-week.
* **Volunteer Referral Tree:** Uses Recursive CTEs to calculate "Influence Points" for volunteer recruitment.
* **Fraud Detection:** Uses `STDDEV` and `AVG` to flag deliveries taking 2 standard deviations longer than average.

## 3. Technology Stack
* **Frontend:** React.js, Tailwind CSS.
* **Backend:** Python (FastAPI/Flask) - *Transitioned from PHP*.
* **Database:** MySQL.