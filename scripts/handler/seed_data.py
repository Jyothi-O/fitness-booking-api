from datetime import datetime
from scripts.db.database import SessionLocal
from scripts.db.db_models import FitnessClass

def seed_data():
    db = SessionLocal()
    if db.query(FitnessClass).first():
        db.close()
        return

    classes = [
        FitnessClass(name="Yoga", instructor="Rita", date_time=datetime(2025, 6, 18, 6, 0), available_slots=5),
        FitnessClass(name="Yoga", instructor="Rita", date_time=datetime(2025, 6, 18, 8, 0), available_slots=4),
        FitnessClass(name="Yoga", instructor="Rita", date_time=datetime(2025, 6, 18, 17, 0), available_slots=3),
        FitnessClass(name="Yoga", instructor="Rita", date_time=datetime(2025, 6, 19, 7, 0), available_slots=3),
        FitnessClass(name="Yoga", instructor="Rita", date_time=datetime(2025, 6, 20, 9, 0), available_slots=2),

        FitnessClass(name="Zumba", instructor="Sam", date_time=datetime(2025, 6, 18, 6, 0), available_slots=4),
        FitnessClass(name="Zumba", instructor="Sam", date_time=datetime(2025, 6, 18, 9, 0), available_slots=3),
        FitnessClass(name="Zumba", instructor="Sam", date_time=datetime(2025, 6, 18, 19, 0), available_slots=5),
        FitnessClass(name="Zumba", instructor="Sam", date_time=datetime(2025, 6, 19, 7, 0), available_slots=3),
        FitnessClass(name="Zumba", instructor="Sam", date_time=datetime(2025, 6, 20, 17, 0), available_slots=6),

        FitnessClass(name="HIIT", instructor="Alex", date_time=datetime(2025, 6, 18, 9, 0), available_slots=4),
        FitnessClass(name="HIIT", instructor="Alex", date_time=datetime(2025, 6, 18, 8, 30), available_slots=3),
        FitnessClass(name="HIIT", instructor="Alex", date_time=datetime(2025, 6, 18, 17, 0), available_slots=4),
        FitnessClass(name="HIIT", instructor="Alex", date_time=datetime(2025, 6, 19, 7, 0), available_slots=3),
        FitnessClass(name="HIIT", instructor="Alex", date_time=datetime(2025, 6, 20, 6, 0), available_slots=4),
    ]

    db.add_all(classes)
    db.commit()
    db.close()
