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
PAYMENTS_ROUTE = "/payments"
CUSTOMER_ROUTE = "/customers"

VALID_ORDER_ID = 3001
INVALID_PAYMENT_ID = 999999

CUSTOMER_TEST_API = {
    "full_name": fake.name(),
    "email": generate_random_email(),
    "phone": generate_cell_phone_number(),
    "address": fake.address(),
    "cpf_cnpj": fake.random_element(elements=[generate_cpf(), generate_cnpj()]),
    "password_hash": generate_password(),
    "role": fake.random_element(elements=["customer", "admin"]),
}

TOKEN = None
HEADERS = {}

CREATED_PAYMENT_ID = None


def test_authenticate_user():
    """authenticate user"""
    global TOKEN, HEADERS

    response = requests.post(URL + CUSTOMER_ROUTE, json=CUSTOMER_TEST_API).json()

    assert response is not None
    assert response == {
        "message": "Customer created successfully!",
        "customer": {"message": "Customer inserted successfully!"},
    }

    login_response = requests.post(
        URL + LOGIN_ROUTE,
        data={
            "username": CUSTOMER_TEST_API["email"],
            "password": CUSTOMER_TEST_API["password_hash"],
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert login_response.status_code == 200
    TOKEN = login_response.json().get("access_token")
    assert TOKEN is not None

    HEADERS = {"Authorization": f"Bearer {TOKEN}"}


def test_create_payment_success():
    """Test creating a payment"""
    global CREATED_PAYMENT_ID

    payload = {
        "order_id": VALID_ORDER_ID,
        "amount": "3500.00",
        "payment_method": "pix",
        "status": "approved",
        "payment_date": datetime.now().isoformat(),
    }

    response = requests.post(URL + PAYMENTS_ROUTE + "/", json=payload, headers=HEADERS)
    json_data = response.json()

    assert response.status_code == 200
    assert json_data["message"] == "Payment created successfully!"
    assert "payment_id" in json_data["payment"]

    CREATED_PAYMENT_ID = json_data["payment"]["payment_id"]


def test_create_payment_invalid_fields():
    """Test creating a payment with invalid fields"""
    invalid_payload = {
        "order_id": "invalid_id",
        "amount": "invalid_amount",
        "payment_method": "crypto",
        "status": "unknown",
        "payment_date": "invalid-date",
    }

    response = requests.post(
        URL + PAYMENTS_ROUTE + "/", json=invalid_payload, headers=HEADERS
    )

    assert response is not None
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "int_parsing",
                "loc": ["body", "order_id"],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": "invalid_id",
            },
            {
                "type": "float_parsing",
                "loc": ["body", "amount"],
                "msg": "Input should be a valid number, unable to parse string as a number",
                "input": "invalid_amount",
            },
            {
                "type": "string_pattern_mismatch",
                "loc": ["body", "payment_method"],
                "msg": "String should match pattern '^(credit_card|pix|boleto|bank_transfer)$'",
                "input": "crypto",
                "ctx": {"pattern": "^(credit_card|pix|boleto|bank_transfer)$"},
            },
            {
                "type": "string_pattern_mismatch",
                "loc": ["body", "status"],
                "msg": "String should match pattern '^(pending|approved|rejected)$'",
                "input": "unknown",
                "ctx": {"pattern": "^(pending|approved|rejected)$"},
            },
            {
                "type": "datetime_from_date_parsing",
                "loc": ["body", "payment_date"],
                "msg": "Input should be a valid datetime or date, invalid character in year",
                "input": "invalid-date",
                "ctx": {"error": "invalid character in year"},
            },
        ]
    }


def test_get_payment_by_valid_id():
    """Test fetching payment by valid ID"""
    response = requests.get(
        f"{URL + PAYMENTS_ROUTE}/?payment_id={CREATED_PAYMENT_ID}", headers=HEADERS
    )

    assert response.status_code == 200
    assert response.json()["id"] == CREATED_PAYMENT_ID


def test_get_payment_by_invalid_id():
    """Test fetching payment by invalid ID"""
    response = requests.get(
        f"{URL + PAYMENTS_ROUTE}/?payment_id={INVALID_PAYMENT_ID}", headers=HEADERS
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Payment not found"}


def test_update_payment_success():
    """Test update of a payment"""
    updated_payload = {
        "order_id": VALID_ORDER_ID,
        "amount": "4000.0",
        "payment_method": "credit_card",
        "status": "approved",
        "payment_date": datetime.now().isoformat(),
    }

    response = requests.put(
        f"{URL + PAYMENTS_ROUTE}/?payment_id={CREATED_PAYMENT_ID}",
        json=updated_payload,
        headers=HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Payment updated successfully"
    assert response.json()["payment"]["payment"][0] == CREATED_PAYMENT_ID
    assert str(response.json()["payment"]["payment"][2]) == updated_payload["amount"]
    assert response.json()["payment"]["payment"][3] == updated_payload["payment_method"]
    assert response.json()["payment"]["payment"][4] == updated_payload["status"]
    assert response.json()["payment"]["payment"][5] == updated_payload["payment_date"]


def test_update_payment_invalid_id():
    """Test update of a non-existent payment"""
    updated_payload = {
        "order_id": VALID_ORDER_ID,
        "amount": "1000.00",
        "payment_method": "pix",
        "status": "pending",
        "payment_date": datetime.now().isoformat(),
    }

    response = requests.put(
        f"{URL + PAYMENTS_ROUTE}/?payment_id={INVALID_PAYMENT_ID}",
        json=updated_payload,
        headers=HEADERS,
    )

    assert response.status_code == 500
    assert response.json() == {"detail": "404: Payment not found or update failed"}


def test_get_payment_unauthorized():
    """Test fetching payment data without authentication"""
    response = requests.get(f"{URL + PAYMENTS_ROUTE}/?payment_id=1")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_delete_payment():
    """Test deleting a payment"""
    response = requests.delete(
        f"{URL + PAYMENTS_ROUTE}/?payment_id={CREATED_PAYMENT_ID}", headers=HEADERS
    )

    assert response.status_code == 405
    assert response.json() == {'detail': 'Method Not Allowed'}