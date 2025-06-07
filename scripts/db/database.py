from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from scripts.db.db_models import Base
from scripts.api_details import app_configuration

# Use file-based SQLite DB for persistence
SQLALCHEMY_DATABASE_URL = app_configuration.DB_FILE

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables once on import/startup
Base.metadata.create_all(bind=engine)
