from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import crud, schemas

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.DeliveryOut)
def create_delivery(delivery: schemas.DeliveryCreate, db: Session = Depends(get_db)):
    # ensure listing exists and volunteer exists
    l = db.query(crud.models.FoodListing).get(delivery.listing_id)
    v = db.query(crud.models.Volunteer).get(delivery.volunteer_id)
    if not l or l.status != 'Available' and l.status != 'Claimed':
        raise HTTPException(status_code=400, detail="Listing not available")
    if not v:
        raise HTTPException(status_code=400, detail="Volunteer not found")
    return crud.create_delivery(db, delivery)

@router.get("/match_nearest")
def match_nearest(lat: float, long: float, db: Session = Depends(get_db)):
    v = crud.find_nearest_volunteer(db, lat, long)
    if not v:
        raise HTTPException(status_code=404, detail="No volunteers with coordinates found")
    return {"volunteer_id": v.volunteer_id, "user_id": v.user_id, "lat": float(v.current_lat), "long": float(v.current_long)}
