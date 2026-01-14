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

@router.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    u = crud.create_user(db, user)
    return u

@router.get("/me", response_model=schemas.UserOut)
def get_me():
    # Placeholder: real auth not implemented yet
    raise HTTPException(status_code=501, detail="Auth not implemented - use /api/users/register and query DB for users")
