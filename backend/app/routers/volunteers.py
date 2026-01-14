from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
def create_volunteer(user_id: int, db: Session = Depends(get_db)):
    u = db.query(models.User).get(user_id)
    if not u or u.user_type != 'Volunteer':
        raise HTTPException(status_code=400, detail='User not found or not a volunteer')
    v = models.Volunteer(user_id=user_id)
    db.add(v)
    db.commit()
    db.refresh(v)
    return {"volunteer_id": v.volunteer_id}

@router.post("/update_location")
def update_location(volunteer_id: int, lat: float, long: float, db: Session = Depends(get_db)):
    v = db.query(models.Volunteer).get(volunteer_id)
    if not v:
        raise HTTPException(status_code=404, detail='Volunteer not found')
    v.current_lat = lat
    v.current_long = long
    db.commit()
    return {"ok": True}

@router.get("/{volunteer_id}")
def get_volunteer(volunteer_id: int, db: Session = Depends(get_db)):
    v = db.query(models.Volunteer).get(volunteer_id)
    if not v:
        raise HTTPException(status_code=404, detail='Volunteer not found')
    return {"volunteer_id": v.volunteer_id, "user_id": v.user_id, "lat": float(v.current_lat) if v.current_lat else None, "long": float(v.current_long) if v.current_long else None}
