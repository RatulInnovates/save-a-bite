from sqlalchemy.orm import Session
from . import models, schemas, utils
from typing import Optional
from datetime import datetime

# Users
def create_user(db: Session, user: schemas.UserCreate):
    hashed = utils.hash_password(user.password)
    db_user = models.User(name=user.name, email=user.email, password_hash=hashed, user_type=user.user_type, zone_id=user.zone_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

# Listings
def create_listing(db: Session, listing: schemas.FoodListingCreate):
    db_listing = models.FoodListing(donor_id=listing.donor_id, food_details=listing.food_details, quantity=listing.quantity, pickup_deadline=listing.pickup_deadline)
    db.add(db_listing)
    db.commit()
    db.refresh(db_listing)
    return db_listing

def list_available(db: Session):
    return db.query(models.FoodListing).filter(models.FoodListing.status == 'Available').all()

# Deliveries
def create_delivery(db: Session, delivery: schemas.DeliveryCreate):
    db_delivery = models.Delivery(listing_id=delivery.listing_id, volunteer_id=delivery.volunteer_id, status='Pending', start_time=datetime.utcnow())
    # Mark listing as claimed
    listing = db.query(models.FoodListing).get(delivery.listing_id)
    if listing:
        listing.status = 'Claimed'
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)
    return db_delivery

# Matching: simple nearest volunteer
def find_nearest_volunteer(db: Session, lat: float, long: float):
    volunteers = db.query(models.Volunteer).filter(models.Volunteer.current_lat != None, models.Volunteer.current_long != None).all()
    best = None
    best_dist = None
    for v in volunteers:
        d = utils.haversine(float(lat), float(long), float(v.current_lat), float(v.current_long))
        if best is None or d < best_dist:
            best = v
            best_dist = d
    return best
