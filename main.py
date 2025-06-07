import uvicorn
from fastapi import FastAPI
from datetime import datetime
from contextlib import asynccontextmanager

from scripts.db.database import SessionLocal, engine
from scripts.db.db_models import Base, FitnessClass
from scripts.api_details import app_configuration
from scripts.service.booking_data_service import booking_router


# Function to seed the database
def seed_data():
    db = SessionLocal()
    existing = db.query(FitnessClass).first()
    if existing:
        db.close()
        return

    classes = [
        FitnessClass(name="Yoga", instructor="Rita", date_time=datetime(2025, 6, 10, 9, 0), available_slots=3),
        FitnessClass(name="Zumba", instructor="Sam", date_time=datetime(2025, 6, 10, 9, 0), available_slots=3),
        FitnessClass(name="HIIT", instructor="Alex", date_time=datetime(2025, 6, 12, 7, 0), available_slots=3),
    ]
    db.add_all(classes)
    db.commit()
    db.close()


# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables and seed data at startup
    Base.metadata.create_all(bind=engine)
    seed_data()
    yield


# Initialize app with lifespan
app = FastAPI(lifespan=lifespan)

# Include your API router(s)
app.include_router(booking_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=app_configuration.SERVICE_HOST,
        port=int(app_configuration.SERVICE_PORT),
        reload=True
    )
