
# Fitness Studio Booking API - Test Scenarios

This document outlines sample test cases for validating the functionality of the **Fitness Studio Booking API**, using the provided seed data.

---

## Seed Data Summary

The fitness studio offers the following classes:

- **Yoga**
- **Zumba**
- **HIIT**

Each class has:
- A unique ID
- An instructor
- A scheduled time (`date_time`)
- A limited number of available slots

---

## Test Cases

---

### 1. Get All Classes

**Endpoint:**  
`GET /classes`

**Description:**  
Retrieves all scheduled classes with available slots.

**Expected Response:**
```json
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
```

---

### 2. Get Classes in Different Timezone

**Endpoint:**  
`GET /classes?timezone=Asia/Dubai`

**Description:**  
Returns all classes with `date_time` adjusted to the specified timezone.

**Expected Response:**
```json
[
  {
    "id": 1,
    "name": "Yoga",
    "date_time": "2025-06-18 04:30"
  },
  ...
]
```

---

### 3. Book Class - Invalid Class ID
Assume class 100 is not available in seed data

**Endpoint:**  
`POST /book`

**Input:**
```json
{
  "class_id": 100,
  "client_name": "John",
  "client_email": "john@gmail.com"
}
```

**Expected Response (400):**
```json
{
  "detail": {
    "message": "Class not found"
  }
}
```

---

### 4. Book Class - Invalid Email

**Endpoint:**  
`POST /book`

**Input:**
```json
{
  "class_id": 100,
  "client_name": "John",
  "client_email": "john"
}
```

**Expected Response (422):**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "client_email"],
      "msg": "value is not a valid email address: The email address is not valid. It must have exactly one @-sign.",
      "input": "john",
      "ctx": {
        "reason": "The email address is not valid. It must have exactly one @-sign."
      }
    }
  ]
}
```

---

### 5. Book Slot for Valid Class

**Endpoint:**  
`POST /book`

**Input:**
```json
{
  "class_id": 1,
  "client_name": "John",
  "client_email": "john@gmail.com"
}
```

**Expected Response (200):**
```json
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
```

---

### 6. Book Slot for Same Time Different Class

**Scenario:**  
User already booked Yoga at 6:00 AM, now tries to book Zumba at the same time.

**Input:**
```json
{
  "class_id": 6,
  "client_name": "John",
  "client_email": "john@gmail.com"
}
```

**Expected Response (400):**
```json
{
  "detail": {
    "message": "You’ve already booked a class at this time. Please choose a different slot/class."
  }
}
```

---

### 7. Book Full Slot

**Scenario:**  
Assume all slots for `class_id = 5` are filled.

**Input:**
```json
{
  "class_id": 5,
  "client_name": "Bob",
  "client_email": "bob@gmail.com"
}
```

**Expected Response (400):**
```json
{
  "detail": {
    "message": "No available slots."
  }
}
```

---

### 8. Get Bookings - Unregistered Email

**Endpoint:**  
`GET /bookings?email=alice@gmail.com`

**Expected Response (404):**
```json
{
  "detail": {
    "message": "No bookings found for email: alice@gmail.com"
  }
}
```

---

### 9. Get Bookings - Registered Email

**Endpoint:**  
`GET /bookings?email=john@gmail.com`

**Expected Response (200):**
```json
[
  {
    "class_id": 1,
    "client_email": "john@gmail.com",
    "date_time": "2025-06-18 06:00",
    "class_name": "Yoga"
  }
]
```

---

## 📌 Notes

- Ensure that your system timezone settings and the FastAPI server align to validate timezone conversions.
- This document assumes the database is seeded with predefined classes and times.
- Booking IDs may differ depending on database state.
