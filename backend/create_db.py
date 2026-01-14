"""Utility to create database tables (uses models metadata.create_all)
Run: python create_db.py (with .env configured)
"""
from app.database import engine, Base
from app import models

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done")
