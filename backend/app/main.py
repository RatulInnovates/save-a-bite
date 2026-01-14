from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database import engine, Base, SessionLocal
from . import models
from .routers import users, listings, deliveries

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SaveABite API")

app.mount("/static", StaticFiles(directory="../frontend"), name="static")

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(listings.router, prefix="/api/listings", tags=["listings"])
app.include_router(deliveries.router, prefix="/api/deliveries", tags=["deliveries"])
# Add volunteers router
from .routers import volunteers
app.include_router(volunteers.router, prefix="/api/volunteers", tags=["volunteers"])
@app.get("/")
def root():
    return {"message": "SaveABite API - visit /static to view frontend"}
