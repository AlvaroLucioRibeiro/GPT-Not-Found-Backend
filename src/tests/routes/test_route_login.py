import os
import requests
from faker import Faker
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from src.tests.utils.utils import (
    generate_random_email,
    generate_password,
    generate_cell_phone_number,
    generate_cpf,
    generate_cnpj,
)

fake = Faker()

# Load environment variables
load_dotenv()

# Definitions for test data
CUSTOMER_TEST_API = {
    "full_name": fake.name(),
    "email": generate_random_email(),
    "phone": generate_cell_phone_number(),  # Adding required field
    "address": fake.address(),  # Adding required field
    "cpf_cnpj": fake.random_element(
        elements=[generate_cpf(), generate_cnpj()]
    ),  # Adding required field
    "password_hash": generate_password(),
    "role": fake.random_element(elements=["customer", "admin"]),
}

URL = "https://gpt-not-found.vercel.app"
LOGIN_ROUTE = "/auth/login"
REGISTER_ROUTE = "/auth/register"
TOKEN = None

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))

# Authentication scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def test_register_customer():
    """
    Tests user registration via API.

    Sends a POST request to register a new user and asserts
    that the response contains a success message.
    """
    response = requests.post(URL + REGISTER_ROUTE, json=CUSTOMER_TEST_API)
    json_response = response.json()

    assert response is not None
    assert "message" in json_response
    assert json_response["message"].startswith("User")
    assert json_response["message"].endswith("registered successfully!")


def test_login_customer():
    """
    Tests user login and token retrieval.

    Sends a POST request to log in with the registered user credentials.
    Asserts that a valid access token is returned.
    """
    login_response = requests.post(
        URL + LOGIN_ROUTE,
        data={
            "username": CUSTOMER_TEST_API["email"],
            "password": CUSTOMER_TEST_API["password_hash"],
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert login_response.status_code == 200, f"Login error: {login_response.json()}"

    json_response = login_response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"

    global TOKEN
    TOKEN = json_response["access_token"]


def test_invalid_login():
    """
    Tests login attempt with invalid credentials.

    Sends a POST request with incorrect login credentials
    and asserts that the API returns an authentication error.
    """
    invalid_response = requests.post(
        URL + LOGIN_ROUTE,
        data={
            "username": CUSTOMER_TEST_API["email"],
            "password": "invalid_password",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert invalid_response.status_code == 400
    assert invalid_response.json()["detail"] == "Invalid email or password"
