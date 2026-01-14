from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP, DECIMAL, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base

class Zone(Base):
    __tablename__ = "zones"
    zone_id = Column(Integer, primary_key=True, index=True)
    zone_name = Column(String(255), nullable=False)

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    otp_code = Column(String(10))
    user_type = Column(String(50), nullable=False)
    zone_id = Column(Integer, ForeignKey("zones.zone_id"))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    donor = relationship("Donor", back_populates="user", uselist=False)
    volunteer = relationship("Volunteer", back_populates="user", uselist=False)

class Donor(Base):
    __tablename__ = "donors"
    donor_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    business_type = Column(String(255))
    hygiene_rating = Column(Integer, default=0)

    user = relationship("User", back_populates="donor")

class Volunteer(Base):
    __tablename__ = "volunteers"
    volunteer_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    travel_distance = Column(DECIMAL(10,2))
    green_points = Column(Integer, default=0)
    current_lat = Column(DECIMAL(10,8))
    current_long = Column(DECIMAL(11,8))
    referrer_id = Column(Integer, ForeignKey("volunteers.volunteer_id"))

    user = relationship("User", back_populates="volunteer")

class FoodListing(Base):
    __tablename__ = "food_listings"
    listing_id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey("donors.donor_id"), nullable=False)
    food_details = Column(Text)
    quantity = Column(String(255))
    pickup_deadline = Column(TIMESTAMP)
    status = Column(String(50), default='Available')
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    donor = relationship("Donor")

class Delivery(Base):
    __tablename__ = "deliveries"
    delivery_id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("food_listings.listing_id"), nullable=False)
    volunteer_id = Column(Integer, ForeignKey("volunteers.volunteer_id"), nullable=False)
    status = Column(String(50), default='Pending')
    start_time = Column(TIMESTAMP)
    end_time = Column(TIMESTAMP)

class LogisticsFund(Base):
    __tablename__ = "logistics_fund"
    transaction_id = Column(Integer, primary_key=True, index=True)
    delivery_id = Column(Integer, ForeignKey("deliveries.delivery_id"), nullable=False)
    sponsor_name = Column(String(255))
    amount = Column(DECIMAL(10,2))
    status = Column(String(50))

class PointsHistory(Base):
    __tablename__ = "points_history"
    point_id = Column(Integer, primary_key=True, index=True)
    volunteer_id = Column(Integer, ForeignKey("volunteers.volunteer_id"), nullable=False)
    point_type = Column(String(50))
    amount = Column(Integer)
    awarded_at = Column(TIMESTAMP, server_default=func.current_timestamp())

class Review(Base):
    __tablename__ = "reviews"
    review_id = Column(Integer, primary_key=True, index=True)
    delivery_id = Column(Integer, ForeignKey("deliveries.delivery_id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    rating = Column(Integer)
    comment = Column(Text)

class Message(Base):
    __tablename__ = "messages"
    message_id = Column(Integer, primary_key=True, index=True)
    delivery_id = Column(Integer, ForeignKey("deliveries.delivery_id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    content = Column(Text, nullable=False)
    sent_at = Column(TIMESTAMP, server_default=func.current_timestamp())
