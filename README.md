
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

## Quickstart (Docker) ✅
1. Copy `.env.example` to `.env` and edit if needed.
2. Run: `docker-compose up --build` — this starts MySQL and the FastAPI app.
3. API: `http://localhost:8000` — Frontend (static): `http://localhost:8000/static`.

## Development (local) ⚙️
Follow these steps to run the app locally on Windows.

1. Create & activate a virtual environment (PowerShell):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate
   ```
2. Install Python dependencies:
   ```powershell
   pip install -r backend/requirements.txt
   ```
3. Start a MySQL database (choose one):
   - Option A — Use Docker (recommended, no local DB install):
     ```powershell
     docker run -d --name saveabite-db -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=saveabite -p 3306:3306 mysql:8.0
     ```
   - Option B — Use a local MySQL server: install MySQL and ensure it is running, then create a database named `saveabite`.
4. Configure environment variables (create `.env` in repo root or set system env vars):
   ```text
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=password
   DB_NAME=saveabite
   ```
5. Create tables and apply schema:
   ```powershell
   python backend/create_db.py
   ```
6. Seed sample data:
   ```powershell
   python backend/seed.py
   ```
7. Run the dev server:
   ```powershell
   uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
   ```
8. Open in your browser:
   - API: `http://localhost:8000` (docs at `http://localhost:8000/docs`)
   - Frontend: `http://localhost:8000/static`

### Run tests
```powershell
pytest -q
```

### Automated setup script (Windows PowerShell)
A helper script is provided to automate local setup: it creates a virtual environment, installs dependencies, starts a MySQL Docker container (optional), creates tables, seeds sample data, and can start the dev server.

Usage (PowerShell, run from repo root):
```powershell
# Run the full setup and start the server
.\scripts\setup-dev.ps1

# Run setup but do not start the server
.\scripts\setup-dev.ps1 -StartServer:$false

# Recreate the DB container if one already exists
.\scripts\setup-dev.ps1 -ForceRestartDB
```

### Troubleshooting & tips
- If the DB connection fails, verify `.env` values and that MySQL is listening on the expected port (3306).
- If `uvicorn` cannot start because the port is in use, stop the process using that port or change `--port`.
- Use the Docker option for the DB to avoid installing MySQL locally.


## Next steps 🔧
- Add auth & JWT, OTP verification, full UI, tests, seeders, background tasks for expiry engine, triggers/procedures as in the proposal.

