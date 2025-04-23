import pytest
import requests
from faker import Faker
from src.tests.utils.utils import (
    generate_cpf,
    generate_cnpj,
    generate_random_email,
    generate_password,
)

fake = Faker()

BASE_URL = "https://gpt-not-found.vercel.app"
LOGIN_ROUTE = "/auth/login"
CUSTOMER_ROUTE = "/customers"
CONTRACT_ROUTE = "/contracts"

TOKEN = None
HEADERS = {}
EVENT_ID = 2001
PDF_FILE_NAME = "test_contract_sample.pdf"
CONTRACT_ID = None

@pytest.fixture(scope="module", autouse=True)
def authenticate_and_set_token():
    """
    Creates a new customer and authenticates to obtain a bearer token.
    """
    global TOKEN, HEADERS

    customer_data = {
        "full_name": fake.name(),
        "email": generate_random_email(),
        "phone": fake.phone_number(),
        "address": fake.address(),
        "cpf_cnpj": fake.random_element(elements=[generate_cpf(), generate_cnpj()]),
        "password_hash": generate_password(),
        "role": "customer",
    }

    response = requests.post(BASE_URL + CUSTOMER_ROUTE, json=customer_data)
    assert response.status_code == 200

    login_response = requests.post(
        BASE_URL + LOGIN_ROUTE,
        data={
            "username": customer_data["email"],
            "password": customer_data["password_hash"],
            "role": customer_data["role"],
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login_response.status_code == 200

    TOKEN = login_response.json().get("access_token")
    assert TOKEN is not None
    HEADERS = {"Authorization": f"Bearer {TOKEN}"}


def test_get_invoice_route_success():
    """Test retrieving an invoice using the order_id."""
    order_id = 3001
    response = requests.get(BASE_URL + f"/invoices/?order_id={order_id}", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["invoice_number"] == "NF-001"

def test_get_invoice_route_not_found():
    """Test retrieving an invoice using a non-existent order_id."""
    order_id = 999999
    response = requests.get(BASE_URL + f"/invoices/?order_id={order_id}", headers=HEADERS)
    assert response.status_code == 404
    assert response.json()["detail"] == "Invoice not found"

def test_download_invoice_route_success():
    """Test retrieving the PDF file path for an invoice using its invoice_id."""
    invoice_id = 7001
    response = requests.get(BASE_URL + f"/invoices/download/?invoice_id={invoice_id}", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["pdf_file"] == "nf_001.pdf"

def test_download_invoice_route_not_found():
    """Test retrieving the PDF file path for a non-existent invoice_id."""
    invoice_id = 999999
    response = requests.get(BASE_URL + f"/invoices/download/?invoice_id={invoice_id}", headers=HEADERS)
    assert response.status_code == 404
    assert response.json()["detail"] == "Invoice PDF not found"
