from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from scripts.api_details.api import Endpoints
from scripts.handler.booking_data_handler import BookingDataHandler
from scripts.models.base_models import DefaultResponse, BookingRequest
from scripts.db.database import get_db
from scripts.logging.log_module import logger as log

booking_router = APIRouter()
handler_obj = BookingDataHandler()


@booking_router.get(Endpoints.classes, response_model=DefaultResponse)
def get_classes_data(
    timezone: str = Query("IST", description="Timezone to view class timings in."),
    db: Session = Depends(get_db)
):
    """
    Fetch all upcoming fitness classes in the provided timezone.
    """
    try:
        result = handler_obj.fetch_classes_data(db, timezone)
        return DefaultResponse(data=result,message="Classes data fetched successfully")
    except Exception as e:
        log.error(f"Error in get_classes_data: {e}")
        raise HTTPException(
            status_code=500,
            detail={"message": "Failed to fetch class data", "error": str(e)}
        )


@booking_router.post(Endpoints.book, response_model=DefaultResponse)
def book_class(
    request: BookingRequest,
    db: Session = Depends(get_db)
):
    """
    Book a spot in a fitness class.
    """
    try:
        result = handler_obj.process_booking(db, request)
        return DefaultResponse(data=result,message="Booking successful")
    except ValueError as ve:
        log.warning(f"Booking issue due to: {ve}")
        raise HTTPException(
            status_code=400,
            detail={"message": "Booking failed", "error": str(ve)}
        )
    except Exception as e:
        log.error(f"Booking failed: {e}")
        raise HTTPException(
            status_code=500,
            detail={"message": "Booking failed", "error": str(e)}
        )


@booking_router.get(Endpoints.bookings, response_model=DefaultResponse)
def get_bookings_by_email(
    email: str = Query(..., description="Email used during booking."),
    db: Session = Depends(get_db)
):
    """
    Retrieve all bookings associated with a specific email.
    """
    try:
        result = handler_obj.fetch_bookings_by_email(db, email)
        if result is None:
            log.info(f"No bookings found for email: {email}")
            raise HTTPException(
                status_code=404,
                detail={"message": f"No bookings found for email: {email}"}
            )
        return DefaultResponse(data=result,message="Bookings data fetched successfully")
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error retrieving bookings for {email}: {e}")
        raise HTTPException(
            status_code=500,
            detail={"message": "Failed to retrieve bookings", "error": str(e)}
        )
