import uvicorn
from fastapi import FastAPI
from datetime import datetime
from contextlib import asynccontextmanager
from scripts.api_details import app_configuration
from scripts.db.database import engine
from scripts.db.db_models import Base
from scripts.handler.seed_data import seed_data
from scripts.service.booking_data_service import booking_router


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
