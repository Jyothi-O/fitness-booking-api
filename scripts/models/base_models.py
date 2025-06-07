from typing import Optional, Any
from pydantic import BaseModel, EmailStr


class DefaultResponse(BaseModel):
    message: Optional[str] = None
    data: Optional[Any] = None


class DefaultFailureResponse(DefaultResponse):
    status: str = "Failed"
    error: Any


class BookingRequest(BaseModel):
    class_id: int
    client_name: str
    client_email: EmailStr
