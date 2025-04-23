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


def test_create_contract():
    """
    Test the creation of a new contract for an existing event.
    """
    global CONTRACT_ID

    contract_payload = {
        "event_id": EVENT_ID,
        "pdf_file": PDF_FILE_NAME,
    }

    response = requests.post(
        BASE_URL + CONTRACT_ROUTE + "/", json=contract_payload, headers=HEADERS
    )
    assert response.status_code == 200

    data = response.json()
    assert "contract_id" in data
    assert data["message"] == "Contract created successfully!"
    CONTRACT_ID = data["contract_id"]


def test_get_contract_by_event_id():
    """
    Test retrieving a contract using the event_id.
    """
    response = requests.get(
        BASE_URL + CONTRACT_ROUTE + f"?event_id={EVENT_ID}", headers=HEADERS
    )
    assert response.status_code == 200

    contract = response.json()
    assert contract["event_id"] == EVENT_ID
    assert contract["pdf_file"] in ["test_contract_sample.pdf", "contrato_001.pdf"]


def test_download_contract_pdf():
    """
    Test downloading the PDF file for a contract using its contract_id.
    """
    assert CONTRACT_ID is not None

    response = requests.get(
        BASE_URL + CONTRACT_ROUTE + f"/download/?contract_id={CONTRACT_ID}",
        headers=HEADERS,
    )
    assert response.status_code == 200
    assert response.json()["pdf_file"] == PDF_FILE_NAME


def test_get_contract_not_found():
    """
    Test retrieving a contract with a non-existent event_id.
    """
    response = requests.get(
        BASE_URL + CONTRACT_ROUTE + "?event_id=999999", headers=HEADERS
    )
    assert response.status_code == 404


def test_download_pdf_not_found():
    """
    Test downloading a PDF for a non-existent contract_id.
    """
    response = requests.get(
        BASE_URL + CONTRACT_ROUTE + "/download/?contract_id=999999",
        headers=HEADERS,
    )
    assert response.status_code == 404
