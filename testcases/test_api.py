from fastapi.testclient import TestClient
from main import app
from scripts.logging.log_module import logger as log
client = TestClient(app)


def test_get_classes():
    response = client.get("/classes")
    log.info(response.json())
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)


def test_book_class_valid():
    # You can change class_id according to your seed data
    payload = {
        "class_id": 1,
        "client_name": "John",
        "client_email": "John@gmail.com"
    }
    response = client.post("/book", json=payload)
    log.info(response.json())
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "confirmed"


def test_book_class_duplicate():
    # Duplicate booking with same email and class_id
    payload = {
        "class_id": 1,
        "client_name": "John",
        "client_email": "John@gmail.com"
    }
    response = client.post("/book", json=payload)
    log.info(response.json())
    assert response.status_code == 400
    assert "already booked" in response.json()["detail"]["error"].lower()


def test_book_class_invalid_email():
    payload = {
        "class_id": 1,
        "client_name": "Bob",
        "client_email": "not-an-email"
    }
    response = client.post("/book", json=payload)
    log.info(response.json())
    assert response.status_code == 422


def test_view_bookings_by_email():
    response = client.get("/bookings", params={"email": "John@gmail.com"})
    log.info(response.json())
    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)
