from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    user_type: str
    zone_id: Optional[int]

class UserOut(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    user_type: str
    zone_id: Optional[int]

    class Config:
        orm_mode = True

class FoodListingCreate(BaseModel):
    donor_id: int
    food_details: str
    quantity: Optional[str]
    pickup_deadline: Optional[datetime]

class FoodListingOut(BaseModel):
    listing_id: int
    donor_id: int
    food_details: str
    quantity: Optional[str]
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

class DeliveryCreate(BaseModel):
    listing_id: int
    volunteer_id: int

class DeliveryOut(BaseModel):
    delivery_id: int
    listing_id: int
    volunteer_id: int
    status: str

    class Config:
        orm_mode = True
