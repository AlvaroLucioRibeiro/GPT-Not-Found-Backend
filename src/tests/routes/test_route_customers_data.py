import requests
from faker import Faker
from src.tests.utils.utils import (
    generate_password,
    generate_cell_phone_number,
    generate_random_email,
    generate_cpf,
    generate_cnpj,
)

# Faker instance for generating test data
fake = Faker()

# API routes and test configuration
URL = "https://gpt-not-found.vercel.app"
LOGIN_ROUTE = "/auth/login"
CUSTOMER_ROUTE = "/customers"
CUSTOMER_DATA_ROUTE = URL + "/customers/1001"  # Assumes customer with ID 1001 exists

# Global variables to store token and headers
TOKEN = None
HEADERS = {}

# Sample customer data for authentication
CUSTOMER_TEST_API = {
    "full_name": fake.name(),
    "email": generate_random_email(),
    "phone": generate_cell_phone_number(),
    "address": fake.address(),
    "cpf_cnpj": fake.random_element(elements=[generate_cpf(), generate_cnpj()]),
    "password_hash": generate_password(),
    "role": fake.random_element(elements=["customer", "admin"]),
}


def test_authenticate_user():
    """
    Authenticate a test user and store the JWT token for authenticated requests.

    This test registers a new customer and logs in to obtain a valid access token.
    """
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
            "role": CUSTOMER_TEST_API["role"],
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert login_response.status_code == 200
    TOKEN = login_response.json().get("access_token")
    assert TOKEN is not None

    HEADERS = {"Authorization": f"Bearer {TOKEN}"}


def test_fetch_customer_events():
    """
    Test fetching all events associated with the given customer.
    """
    response = requests.get(CUSTOMER_DATA_ROUTE + "/events", headers=HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_fetch_customer_orders():
    """
    Test fetching all orders associated with the given customer.
    """
    response = requests.get(CUSTOMER_DATA_ROUTE + "/orders", headers=HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_fetch_customer_payments():
    """
    Test fetching all payments associated with the given customer.
    """
    response = requests.get(CUSTOMER_DATA_ROUTE + "/payments", headers=HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_fetch_customer_invoices():
    """
    Test fetching all invoices associated with the given customer.
    """
    response = requests.get(CUSTOMER_DATA_ROUTE + "/invoices", headers=HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_fetch_customer_contracts():
    """
    Test fetching all contracts associated with the given customer.
    """
    response = requests.get(CUSTOMER_DATA_ROUTE + "/contracts", headers=HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_fetch_customer_order_items():
    """
    Test fetching all order items associated with the given customer.
    """
    response = requests.get(CUSTOMER_DATA_ROUTE + "/order_items", headers=HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
