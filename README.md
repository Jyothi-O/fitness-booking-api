# Fitness Class Booking API

A simple FastAPI application that allows users to:

- View available fitness classes
- Book a class
- View bookings by email

This project demonstrates good design practices (modularity, validations, timezone management) and is perfect for showcasing backend development skills.

---

## Features

- View upcoming fitness classes
- Book a spot in a class
- Prevent double bookings
- View bookings by email
- Input validations (e.g. valid email, fields required)
- Timezone support (IST-based, converts on request)
- Handles overbooking scenarios
- In-memory or file-based SQLite DB supported

---

## Tech Stack

- Python 3.9+
- FastAPI
- SQLAlchemy
- SQLite (file-based by default)
- Pydantic
- Uvicorn (ASGI server)
- ZoneInfo & Pytz (for timezone conversions)

---

## Getting Started

### 1.Clone the Repository

```bash
git clone https://github.com/Jyothi-O/fitness-booking-api.git
cd fitness-booking-api
```

### 2.Create Virtual Environment (optional)

```bash
python -m venv venv
source venv/bin/activate   # For Linux/macOS
venv\Scripts\activate      # For Windows
```

### 3.Install Dependencies

```bash
pip install -r requirements.txt
```

> If you're using email validation:
```bash
pip install "pydantic[email]"
```

### 4.Run the Application

```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload

```
## Seed Data

The fitness studio booking API comes preloaded with sample classes to help you test and explore the functionality easily. This seed data is located in the file: **seed_data.py**

It includes Yoga, Zumba, and HIIT classes scheduled across multiple days with varied timings and available slots.

The data is stored in a local SQLite database file named: **fitness_booking.db**

This fitness_booking.db file is created automatically when you start the app.

### Class Schedule Overview

| Class Type | Date       | Time  | Available Slots | Instructor |
|------------|------------|-------|-----------------|------------|
| Yoga       | 2025-06-18 | 06:00 | 5               | Rita       |
| Yoga       | 2025-06-18 | 08:00 | 4               | Rita       |
| Yoga       | 2025-06-18 | 17:00 | 3               | Rita       |
| Yoga       | 2025-06-19 | 07:00 | 3               | Rita       |
| Yoga       | 2025-06-20 | 09:00 | 2               | Rita       |
| Zumba      | 2025-06-18 | 07:00 | 4               | Sam        |
| Zumba      | 2025-06-18 | 09:00 | 3               | Sam        |
| Zumba      | 2025-06-18 | 19:00 | 5               | Sam        |
| Zumba      | 2025-06-19 | 07:00 | 3               | Sam        |
| Zumba      | 2025-06-20 | 17:00 | 6               | Sam        |
| HIIT       | 2025-06-18 | 08:30 | 3               | Alex       |
| HIIT       | 2025-06-18 | 09:00 | 4               | Alex       |
| HIIT       | 2025-06-18 | 17:00 | 4               | Alex       |
| HIIT       | 2025-06-19 | 07:00 | 3               | Alex       |
| HIIT       | 2025-06-20 | 06:00 | 4               | Alex       |

### How to load seed data

The data is automatically seeded into the database when you start the app. To start the server and have this data loaded, run:

```bash
uvicorn main:app --reload
```

## Testing the API

Once running, you can explore the API docs at `http://localhost:8080/docs` for interactive testing.

Example curl request to get classes:

```bash
curl -X GET "http://localhost:8080/classes"
```

## Project Structure
```
.
├── conf/
│   └── application.conf           # Application-level config (DB path, logging, service host/port, etc.)
│
├── scripts/
│   ├── api_details/               # API endpoint path definitions and configuration
│   │   ├── api.py
│   │   └── app_configuration.py   # Config parser for reading application.conf
│   │
│   ├── db/
│   │   ├── database.py            # DB engine and session setup (SQLite)
│   │   └── db_models.py           # SQLAlchemy models: FitnessClass, Booking
│   │
│   ├── handler/
│   │   ├── booking_data_handler.py # Business logic handling API requests, validation
│   │   └── seed_data.py            # Seed data script to initialize sample fitness classes
│   │
│   ├── logging/
│   │   └── log_module.py          # Centralized logging configuration and logger setup
│   │
│   ├── models/
│   │   └── base_models.py         # Pydantic schemas for request and response validation
│   │
│   └── service/
│       └── booking_service.py     # Service layer with reusable DB operations and helpers
│
├── docs/
│   └── test_scenarios.md          # Contains all detailed API test scenarios and expected outcomes
│
├── testcases/
│   └── test_api.py                # Basic automated test cases using pytest or similar
│
├── main.py                        # Application startup, DB initialization, router inclusion, seed data loading
├── requirements.txt               # Python dependencies required to run the project
└── README.md                      # Project documentation, instructions, and overview

```

---

## API Endpoints

### Get All Upcoming Classes

```http
GET /classes
```

#### Query Params:
- `timezone` (default: IST)

#### Response:
```json
{
  "data": [
    {
      "id": 1,
      "name": "Yoga",
      "instructor": "Rita",
      "date_time": "2025-06-18 06:00",
      "available_slots": 5
    }
  ]
}
```

---

### Book a Class

```http
POST /book
```

#### Request Body:
```json
{
  "class_id": 1,
  "client_name": "John",
  "client_email": "john@gmail.com"
}
```

#### Validations:
- Email format check
- Class existence
- Available slots
- Prevent duplicate bookings

#### Response:
```json
{
  "data": {
    "booking_id": 1,
    "class_id": 1,
    "client_name": "John",
    "client_email": "john@gmail.com",
    "status": "confirmed"
  }
}
```

---

### View Bookings by Email

```http
GET /bookings?email=john@gmail.com
```

#### Response:
```json
{
  "data": [
    {
      "booking_id": 1,
      "class_id": 1,
      "class_name": "Yoga",
      "slot_time": "2025-06-18 06:00",
      "client_name": "John",
      "client_email": "john@gmail.com"
    }
  ]
}
```

---

## Validation & Error Handling

- Proper error messages for:
  - Invalid email
  - Class not found
  - Overbooking
  - Duplicate booking
- Timezone fallback to IST if invalid timezone provided
- HTTP status codes: `400`, `404`, `500`

---

## Test Scenarios and Test Cases

### 📄 Detailed Test Scenarios

All possible API test scenarios, including sample inputs and expected outputs, are documented in:

- `docs/test_scenarios.md`

### Automated API Tests

Basic automated tests for core functionality are included in:

- `testcases/test_api.py`

These tests can be executed using `pytest` to ensure the API endpoints are working as expected.

> Run using:
```bash
pytest testcases/test_api.py
