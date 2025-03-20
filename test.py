import pytest
import requests
from faker import Faker
from src.tests.utils.utils import generate_random_email, generate_cpf, generate_cnpj

fake = Faker()

CUSTOMER_TEST_API = {
    "full_name": "teste2@gmail.com",
    "email": "teste2@gmail.com",
    "phone": fake.phone_number(),
    "address": fake.address(),
    "cpf_cnpj": fake.random_element(elements=[generate_cpf(), generate_cnpj()]),
    "password_hash": "teste!@#123",
    "role": fake.random_element(elements=["customer", "admin"]),
}

CUSTOMER_TEST_API_LOGGED = None

URL = "https://gpt-not-found.vercel.app"

LOGIN_ROUTE = "/auth/login"

CUSTOMER_ROUTE = "customers"


def login_request(email, password):
    return requests.post(
        URL + LOGIN_ROUTE,
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

if __name__ == "__main__":
    response = login_request(CUSTOMER_TEST_API["email"], CUSTOMER_TEST_API["password_hash"])
    print(response.status_code)
    print(response.text)