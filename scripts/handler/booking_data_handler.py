from zoneinfo import ZoneInfo
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from scripts.logging.log_module import logger as log
from datetime import datetime
from scripts.db.db_models import FitnessClass, Booking


class BookingDataHandler:
    """
    Handles logic for retrieving classes, booking slots, and viewing bookings.
    """

    def fetch_classes_data(self, db: Session, timezone: str):
        """
        Get all upcoming fitness classes, converting date_time to requested timezone.

        Args:
            db (Session): SQLAlchemy DB session.
            timezone (str): Desired timezone string.

        Returns:
            list: List of upcoming classes.
        """
        try:
            ist = ZoneInfo("Asia/Kolkata")
            tz = ZoneInfo(timezone)
        except Exception:
            tz = ist
            log.warning(f"Invalid timezone '{timezone}' provided. Defaulting to IST.")

        try:
            now_ist = datetime.now(ZoneInfo("Asia/Kolkata"))
            classes = db.query(FitnessClass).filter(FitnessClass.date_time >= now_ist).all()

            result = [{
                "id": cls.id,
                "name": cls.name,
                "instructor": cls.instructor,
                "date_time": cls.date_time.replace(tzinfo=ist).astimezone(tz).strftime("%Y-%m-%d %H:%M"),
                "available_slots": cls.available_slots
            } for cls in classes]

            log.info(f"{len(result)} upcoming class(es) fetched successfully.")
            return result

        except Exception as e:
            log.error(f"Error fetching classes: {e}")
            raise Exception("Could not retrieve class data.")

    from sqlalchemy.orm import Session
    from sqlalchemy.exc import SQLAlchemyError
    from datetime import datetime
    from scripts.logging.log_module import logger as log
    from scripts.db.db_models import FitnessClass, Booking

    def process_booking(self, db: Session, request):
        """
        Book a class if slots are available and user has no conflicting bookings.

        Args:
            db (Session): SQLAlchemy DB session.
            request: Pydantic model with class_id, client_name, client_email.

        Returns:
            dict: Confirmation details.
        """
        try:
            # Fetch class details
            fitness_class = db.query(FitnessClass).filter(FitnessClass.id == request.class_id).first()
            if not fitness_class:
                log.warning(f"Class ID {request.class_id} not found.")
                raise ValueError("Class not found.")

            # Check if class is full
            if fitness_class.available_slots <= 0:
                log.info(f"No slots left for class ID {request.class_id}.")
                raise ValueError("No available slots.")

            # Check if user has already booked the same class at the same time
            existing_booking = (
                db.query(Booking)
                .join(FitnessClass, Booking.class_id == FitnessClass.id)
                .filter(
                    Booking.client_email == request.client_email,
                    FitnessClass.date_time == fitness_class.date_time
                )
                .first()
            )
            if existing_booking:
                log.info(f"User {request.client_email} already booked a class at {fitness_class.date_time}.")
                raise ValueError("You’ve already booked a class at this time. Please choose a different slot/class.")

            # Proceed with booking
            fitness_class.available_slots -= 1
            db.commit()

            booking = Booking(
                class_id=request.class_id,
                client_name=request.client_name,
                client_email=request.client_email,
                booking_time=datetime.now()
            )
            db.add(booking)
            db.commit()
            db.refresh(booking)

            log.info(f"Booking confirmed: {booking.id} for {request.client_email} at {fitness_class.date_time}")

            return {
                "booking_id": booking.id,
                "class_id": request.class_id,
                "client_name": request.client_name,
                "client_email": request.client_email,
                "status": "confirmed"
            }

        except (SQLAlchemyError, ValueError) as e:
            db.rollback()
            log.error(f"Booking failed for {request.client_email}: {e}")
            raise

    def fetch_bookings_by_email(self, db: Session, email: str):
        """
        Get all bookings for a given email.

        Args:
            db (Session): SQLAlchemy DB session.
            email (str): Client's email ID.

        Returns:
            list | None: Booking list or None if not found.
        """
        try:
            bookings = db.query(Booking).filter(Booking.client_email == email).all()
            if not bookings:
                return None

            result = []
            for b in bookings:
                fitness_class = db.query(FitnessClass).filter(FitnessClass.id == b.class_id).first()
                slot_time = fitness_class.date_time.strftime("%Y-%m-%d %H:%M") if fitness_class else "N/A"

                result.append({
                    "booking_id": b.id,
                    "class_id": b.class_id,
                    "class_name": b.fitness_class.name,
                    "client_name": b.client_name,
                    "client_email": b.client_email,
                    "slot_time": slot_time,
                })

            log.info(f"Found {len(result)} bookings for {email}")
            return result
        except Exception as e:
            log.error(f"Failed to fetch bookings for {email}: {e}")
            raise
