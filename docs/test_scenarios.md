Fitness Studio Booking API - Test Scenarios

This document contains sample inputs and expected responses for validating the Fitness Studio Booking API functionality based on the predefined seed data.

Seed Data Summary

Classes are offered across three types: Yoga, Zumba, and HIIT.Each class has an instructor, scheduled time, and available slots.

Test Cases

1. Get All Classes

Endpoint: GET /classes

Input:

GET /classes

Expected Response (200):

[
  {
    "id": 1,
    "name": "Yoga",
    "instructor": "Rita",
    "date_time": "2025-06-18 06:00",
    "available_slots": 5
  },
  ...
]

2. Get Classes in Different Timezone

Endpoint: GET /classes?timezone=Asia/Dubai

Expected Response (200):
All date_time values adjusted to Asia/Dubai timezone.

[
  {
    "id": 1,
    "name": "Yoga",
    "date_time": "2025-06-18 04:30"
  },
  ...
]

3. Book Class - Invalid Class ID

Endpoint: POST /book

Input:

{
  "class_id": 100,
  "client_name": "John",
  "client_email": "john@gmail.com"
}

Expected Response (400):

{
  "detail": {
    "message": "Booking failed",
    "error": "Class not found."
  }
}

4. Book Class - Invalid Email

Endpoint: POST /book

Input:

{
  "class_id": 100,
  "client_name": "John",
  "client_email": "john"
}

Expected Response (422):

{
  "detail": [
    {
      "type": "value_error",
      "loc": [
        "body",
        "client_email"
      ],
      "msg": "value is not a valid email address: The email address is not valid. It must have exactly one @-sign.",
      "input": "john",
      "ctx": {
        "reason": "The email address is not valid. It must have exactly one @-sign."
      }
    }
  ]
}

5. Book Slot for Valid Class

Input:

{
  "class_id": 1,
  "client_name": "John",
  "client_email": "john@gmail.com"
}

Expected Response (200):

{
  "message": "Booking successful",
  "data": {
    "booking_id": 2,
    "class_id": 1,
    "client_name": "John",
    "client_email": "john@gmail.com",
    "status": "confirmed"
  }
}

6. Book Slot for Same Time Different Class

Input:
User already booked Yoga class at 6 AM, now trying to book Zumba at same time.

{
  "class_id": 6,
  "client_name": "John",
  "client_email": "john@gmail.com"
}

Expected Response (400):

{
  "detail": {
    "message": "Booking failed",
    "error": "You’ve already booked a class at this time. Please choose a different slot/class."
  }
}

6.  Book Full Slot

(Assume all slots for class_id = 5 are filled)

{
  "class_id": 5,
  "client_name": "Bob",
  "client_email": "bob@gmail.com"
}

Expected Response (400):

{
  "detail": {
    "message": "No available slots."
  }
}

7.  Get Bookings - Unregistered Email

Endpoint: GET /bookings?email=alice@gmail.com

Expected Response (404):

{
  "detail": {
    "message": "No bookings found for email: alice@gmail.com"
  }
}

8.  Get Bookings - Registered Email

Endpoint: GET /bookings?email=john@gmail.com

Expected Response (200):

[
  {
    "class_id": 1,
    "client_email": "alice@example.com",
    "date_time": "2025-06-18 06:00",
    "class_name": "Yoga"
  }
]


