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

@router.post("/", response_model=schemas.FoodListingOut)
def create_listing(listing: schemas.FoodListingCreate, db: Session = Depends(get_db)):
    return crud.create_listing(db, listing)

@router.get("/available", response_model=list[schemas.FoodListingOut])
def available(db: Session = Depends(get_db)):
    return crud.list_available(db)
