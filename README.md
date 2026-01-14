
# save-a-bite
=======
# 🥗 SaveABite: Food Security & Waste Reduction System

**SaveABite** is a hyper-local web-based marketplace designed to bridge the logistical gap between food surplus and food insecurity in Bangladesh. It connects food donors (restaurants, convention centers) with distribution units (NGOs, volunteers) to ensure surplus food reaches those in need before it spoils.

## 🎯 Project Overview
Unlike simple listing sites, SaveABite is an **automated logistics engine**. It uses database-driven logic to match donors with nearby volunteers, verify food safety via hygiene ratings, and manage timely deliveries. The project is aligned with **SDG 2 (Zero Hunger)** and **SDG 12 (Responsible Consumption)**.

## ✨ Key Features
* **Automated Volunteer Matching:** Uses logic to match a `Food_Listing` with the nearest volunteer based on location.
* **Real-Time Expiry Engine:** A MySQL Event Scheduler runs every 15 minutes to auto-expire listings if the pickup time has passed.
* **Gamification & Rewards:** "Green Points" are automatically awarded to volunteers via database triggers upon successful delivery validation via OTP scan.
* **Monetary Logistics Fund:** Manages a fund where the public can sponsor specific ride costs (e.g., rickshaw fares) for volunteers using ACID transactions.
* **Dual-Layer Verification:** A rating system where volunteers rate donor hygiene, and donors verify volunteer arrival via OTP.
* **Advanced Analytics:** * **Zonal Leaderboards:** Ranks volunteers dynamically based on monthly performance using SQL Window Functions.
    * **Waste Trend Analytics:** Compares a donor's food waste generation week-over-week.
    * **Fraud Detection:** Flags deliveries that take significantly longer than the average time for a specific distance.
    * **Referral Tree:** Uses Recursive CTEs to calculate "Influence Points" for volunteers who invite others.

## 🏗️ Tech Stack
* **Frontend:** React.js, Tailwind CSS.
* **Backend:** Python (FastAPI/Flask).
* **Database:** MySQL.
* **Design:** Figma.

## 📊 Database Schema
The system architecture includes several interconnected entities to manage the rescue lifecycle:
* **Users & Zones:** Categorizes users into Donors and Volunteers across specific geographic zones.
* **Food Listings:** Tracks food details, hygiene ratings, and pickup deadlines.
* **Deliveries:** Orchestrates the handoff and status tracking between donors and volunteers.
* **Gamification:** Tracks `green_points` and `points_history` for volunteer engagement.
* **Communication:** Internal `messages` system to protect user privacy.

## 🛡

