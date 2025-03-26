import pytest
import requests
from faker import Faker
from src.db.CRUD.create import create_customer
from src.db.CRUD.update import update_customer
from src.db.CRUD.delete import delete_customer
from src.tests.utils.utils import generate_random_email, generate_cpf, generate_cnpj
from src.db.CRUD.read import (
    get_customer_by_id,
    get_all_customers,
    get_customer_by_email,
)

fake = Faker()

CUSTOMER_TEST_API = {
    "full_name": fake.name(),
    "email": generate_random_email(),
    "phone": fake.phone_number(),
    "address": fake.address(),
    "cpf_cnpj": fake.random_element(elements=[generate_cpf(), generate_cnpj()]),
    "password_hash": "senha123",
    "role": fake.random_element(elements=["customer", "admin"]),
}

CUSTOMER_TEST_API_MOCK = {
    "email": "teste2@gmail.com",
    "password_hash": "teste!@#123",
}

CUSTOMER_TEST_API_LOGGED = None

URL = "https://gpt-not-found.vercel.app"

LOGIN_ROUTE = "/auth/login"

CUSTOMER_ROUTE = "/auth/register"


def test_create_customer():
    """Test creating a new customer by the API"""

    response = requests.post(URL + CUSTOMER_ROUTE, json=CUSTOMER_TEST_API).json()

    assert response is not None
    assert response["message"] ==  f"User {CUSTOMER_TEST_API['full_name']} registered successfully!"
    # assert response == {
    #     "message": "Customer created successfully!",
    #     "customer": {"message": "Customer inserted successfully!"},
    # }


def test_get_customer_data_by_email():
    """Test getting a customer by email with authentication"""

    # Step 1: Obter o token de autenticação
    login_response = requests.post(
        URL + LOGIN_ROUTE,
        data={
            "username": CUSTOMER_TEST_API["email"],
            "password": CUSTOMER_TEST_API["password_hash"],
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    print(CUSTOMER_TEST_API["email"])
    print(CUSTOMER_TEST_API["password_hash"])

    # # Step 1: Obter o token de autenticação mockado
    # login_response = requests.post(
    #     URL + LOGIN_ROUTE,
    #     data={
    #         "username": CUSTOMER_TEST_API_MOCK["email"],
    #         "password": CUSTOMER_TEST_API_MOCK["password_hash"],
    #     },
    #     headers={"Content-Type": "application/x-www-form-urlencoded"},
    # )

    # print("Status Code:", login_response.status_code)
    # print("Response Body:", login_response.text)

    print(login_response)

    assert login_response.status_code == 200
    token = login_response.json().get("access_token")
    assert token, "Nenhum token de autenticação retornado"

    # Step 2: Fazer a requisição autenticada para obter os dados do cliente
    # headers = {"Authorization": f"Bearer {token}"}
    # route = f"/customers?customer_id={CUSTOMER_TEST_API['email']}"
    # response = requests.get(URL + route, headers=headers).json()

    # assert response is not None
    # assert response == CUSTOMER_TEST_API
    # assert response["email"] == CUSTOMER_TEST_API["email"]

    # # Definir os dados globais para os próximos testes
    # global CUSTOMER_TEST_API_LOGGED
    # CUSTOMER_TEST_API_LOGGED = response


def test_get_all_customers():
    """Test getting all customers returned by the API"""

    route = "/customers"
    response = requests.get(URL + route).json()

    assert response is not None
    assert len(response) > 0
