from app.database import SessionLocal, engine, Base
from app import models, utils

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Seed zones
zones = ['Dhaka North', 'Dhaka South', 'Chittagong']
for z in zones:
    if not db.query(models.Zone).filter(models.Zone.zone_name==z).first():
        db.add(models.Zone(zone_name=z))

# Simple users and profiles
if not db.query(models.User).filter(models.User.email=='donor1@example.com').first():
    u1 = models.User(name='Donor One', email='donor1@example.com', password_hash=utils.hash_password('password'), user_type='Donor')
    db.add(u1)
    db.flush()
    db.add(models.Donor(user_id=u1.user_id, business_type='Restaurant'))

if not db.query(models.User).filter(models.User.email=='vol1@example.com').first():
    u2 = models.User(name='Volunteer One', email='vol1@example.com', password_hash=utils.hash_password('password'), user_type='Volunteer')
    db.add(u2)
    db.flush()
    db.add(models.Volunteer(user_id=u2.user_id, current_lat=23.7808875, current_long=90.2792371, green_points=10))

# Sample listing
donor = db.query(models.Donor).join(models.User).filter(models.User.email=='donor1@example.com').first()
if donor and not db.query(models.FoodListing).first():
    db.add(models.FoodListing(donor_id=donor.donor_id, food_details='30 kg cooked rice', quantity='30 kg'))

db.commit()
print('Seed complete')
