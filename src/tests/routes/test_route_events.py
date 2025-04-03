import requests
from faker import Faker
from datetime import datetime
from src.tests.utils.utils import (
    generate_password,
    generate_cell_phone_number,
    generate_random_email,
    generate_cpf,
    generate_cnpj,
)

fake = Faker()

URL = "https://gpt-not-found.vercel.app"
LOGIN_ROUTE = "/auth/login"
CUSTOMER_ROUTE = "/customers"
EVENTS_ROUTE = "/events"

TOKEN = None
HEADERS = {}
CREATED_EVENT_ID = None
INVALID_EVENT_ID = 999999

CUSTOMER_TEST_API = {
    "full_name": fake.name(),
    "email": generate_random_email(),
    "phone": generate_cell_phone_number(),
    "address": fake.address(),
    "cpf_cnpj": fake.random_element(elements=[generate_cpf(), generate_cnpj()]),
    "password_hash": generate_password(),
    "role": "customer",
}


def test_authenticate_user():
    """Authenticate and store token"""
    global TOKEN, HEADERS

    response = requests.post(URL + CUSTOMER_ROUTE, json=CUSTOMER_TEST_API).json()
    assert response["message"] == "Customer created successfully!"

    login_response = requests.post(
        URL + LOGIN_ROUTE,
        data={
            "username": CUSTOMER_TEST_API["email"],
            "password": CUSTOMER_TEST_API["password_hash"],
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    TOKEN = login_response.json().get("access_token")
    assert TOKEN is not None
    HEADERS = {"Authorization": f"Bearer {TOKEN}"}


def test_create_event_success():
    """Test creating an event successfully"""
    global CREATED_EVENT_ID

    payload = {
        "customer_id": 1001,
        "event_type": "debutante",
        "event_date": "2025-12-01T20:00:00",
        "location": "Espaço Glamour",
        "guest_count": 120,
        "duration_hours": 5,
        "budget_approved": True,
    }

    response = requests.post(URL + EVENTS_ROUTE + "/", json=payload, headers=HEADERS)
    json_data = response.json()

    assert response.status_code == 200
    assert json_data["message"] == "Event successfully created!"
    assert "event_id" in response.text

    CREATED_EVENT_ID = json_data["event_id"]

    # Verifica se o evento foi criado corretamente
    fetch = requests.get(
        f"{URL + EVENTS_ROUTE}/?event_id={CREATED_EVENT_ID}", headers=HEADERS
    )
    assert fetch.status_code == 200
    assert fetch.json()["location"] == payload["location"]


def test_create_event_invalid_fields():
    """Test creating event with invalid values"""
    payload = {
        "customer_id": "invalid",
        "event_type": "random",
        "event_date": "invalid-date",
        "location": 12345,
        "guest_count": "ten",
        "duration_hours": "five",
        "budget_approved": "yes",
    }

    response = requests.post(URL + EVENTS_ROUTE + "/", json=payload, headers=HEADERS)
    assert response.status_code == 422


def test_get_event_by_valid_id():
    """Test fetching a valid event"""
    global CREATED_EVENT_ID
    assert CREATED_EVENT_ID is not None

    response = requests.get(
        f"{URL + EVENTS_ROUTE}/?event_id={CREATED_EVENT_ID}", headers=HEADERS
    )

    assert response.status_code == 200
    assert response.json()["id"] == CREATED_EVENT_ID


def test_get_event_by_invalid_id():
    """Test fetching an invalid event"""
    response = requests.get(
        f"{URL + EVENTS_ROUTE}/?event_id={INVALID_EVENT_ID}", headers=HEADERS
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Event not found"}


def test_update_event_success():
    """Test updating a valid event"""
    global CREATED_EVENT_ID
    assert CREATED_EVENT_ID is not None

    payload = {
        "event_type": "wedding",
        "event_date": "2025-12-31T22:00:00",
        "location": "Villa Lobos Hall",
        "guest_count": 200,
        "duration_hours": 6,
        "budget_approved": False,
    }

    response = requests.put(
        f"{URL + EVENTS_ROUTE}/?event_id={CREATED_EVENT_ID}",
        json=payload,
        headers=HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Event updated successfully"


def test_update_event_invalid_id():
    """Test updating a non-existent event"""
    payload = {
        "event_type": "corporate",
        "event_date": "2025-11-20T19:00:00",
        "location": "Fazenda Aurora",
        "guest_count": 80,
        "duration_hours": 3,
        "budget_approved": True,
    }

    response = requests.put(
        f"{URL + EVENTS_ROUTE}/?event_id={INVALID_EVENT_ID}",
        json=payload,
        headers=HEADERS,
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Event not found"}


def test_get_event_unauthorized():
    """Test unauthorized access to event"""
    response = requests.get(f"{URL + EVENTS_ROUTE}/?event_id=1")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_delete_event_success():
    """Test deleting an event"""
    global CREATED_EVENT_ID
    assert CREATED_EVENT_ID is not None

    response = requests.delete(
        f"{URL + EVENTS_ROUTE}/?event_id={CREATED_EVENT_ID}", headers=HEADERS
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Event deleted successfully"}


def test_delete_event_invalid_id():
    """Test deleting an invalid event"""
    response = requests.delete(
        f"{URL + EVENTS_ROUTE}/?event_id={INVALID_EVENT_ID}", headers=HEADERS
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Event not found"}
