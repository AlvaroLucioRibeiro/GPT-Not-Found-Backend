import requests
from faker import Faker
from src.tests.utils.utils import (
    generate_random_email,
    generate_cpf,
    generate_cnpj,
    generate_password,
    generate_cell_phone_number,
)

fake = Faker()

CUSTOMER_TEST_API = {
    "full_name": fake.name(),
    "email": generate_random_email(),
    "phone": generate_cell_phone_number(),
    "address": fake.address(),
    "cpf_cnpj": fake.random_element(elements=[generate_cpf(), generate_cnpj()]),
    "password_hash": generate_password(),
    "role": fake.random_element(elements=["customer", "admin"]),
}

CUSTOMER_TEST_API_LOGGED = None

TOKEN = None

URL = "https://gpt-not-found.vercel.app"

LOGIN_ROUTE = "/auth/login"

CUSTOMER_ROUTE = "/customers"


def test_create_customer():
    """Test creating a new customer by the API"""

    response = requests.post(URL + CUSTOMER_ROUTE, json=CUSTOMER_TEST_API).json()

    assert response is not None
    assert response == {
        "message": "Customer created successfully!",
        "customer": {"message": "Customer inserted successfully!"},
    }


def test_create_customer_invalid_email():
    """Test customer creation with invalid email"""
    invalid_data = CUSTOMER_TEST_API.copy()
    invalid_data["email"] = "invalid-email"

    response = requests.post(URL + CUSTOMER_ROUTE, json=invalid_data)

    assert response is not None
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "value_error",
                "loc": ["body", "email"],
                "msg": "value is not a valid email address: An email address must have an @-sign.",
                "input": "invalid-email",
                "ctx": {"reason": "An email address must have an @-sign."},
            }
        ]
    }


def test_create_customer_weak_password():
    """Test customer creation with weak password"""
    invalid_data = CUSTOMER_TEST_API.copy()
    invalid_data["password_hash"] = "123"

    response = requests.post(URL + CUSTOMER_ROUTE, json=invalid_data)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "The password must be at least 6 characters long."
    }


def test_get_customer_data_by_invalid_token():
    """Test fetching customer data with invalid token"""
    headers = {"Authorization": "Bearer invalid.token.here"}

    response = requests.get(URL + CUSTOMER_ROUTE + "/me", headers=headers)

    assert response.status_code == 401


def test_get_customer_by_nonexistent_id():
    """Test fetching customer by non-existent ID"""
    headers = {"Authorization": f"Bearer {TOKEN}"}
    route = f"{CUSTOMER_ROUTE}?customer_id=999999"

    response = requests.get(URL + route, headers=headers)

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test_update_customer_not_found():
    """Test updating a non-existent customer"""
    headers = {"Authorization": f"Bearer {TOKEN}"}
    route = f"{CUSTOMER_ROUTE}?customer_id=999999"

    data = CUSTOMER_TEST_API.copy()
    response = requests.put(URL + route, json=data, headers=headers)

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test_delete_customer_not_found():
    """Test deleting a non-existent customer"""
    headers = {"Authorization": f"Bearer {TOKEN}"}
    route = f"{CUSTOMER_ROUTE}?customer_id=999999"

    response = requests.delete(URL + route, headers=headers)

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test_get_customer_data_by_token():
    """Test getting a customer by token"""

    # Take the token based on the login
    login_response = requests.post(
        URL + LOGIN_ROUTE,
        data={
            "username": CUSTOMER_TEST_API["email"],
            "password": CUSTOMER_TEST_API["password_hash"],
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert login_response.status_code == 200
    token = login_response.json().get("access_token")
    assert token, "Nenhum token de autenticação retornado"

    customer_me = requests.get(
        URL + CUSTOMER_ROUTE + "/me",
        headers={"Authorization": f"Bearer {token}"},
    ).json()

    assert customer_me is not None
    assert customer_me["user"]["email"] == CUSTOMER_TEST_API["email"]
    assert customer_me["user"]["role"] == CUSTOMER_TEST_API["role"]
    assert customer_me["user"]["full_name"] == CUSTOMER_TEST_API["full_name"]
    assert customer_me["user"]["phone"] == CUSTOMER_TEST_API["phone"]
    assert customer_me["user"]["address"] == CUSTOMER_TEST_API["address"]

    global TOKEN
    TOKEN = token

    global CUSTOMER_TEST_API_LOGGED
    CUSTOMER_TEST_API_LOGGED = customer_me["user"]


def test_get_customer_data_by_id():
    """Test getting a customer by id returned by the API"""

    headers = {"Authorization": f"Bearer {TOKEN}"}
    route = f"{CUSTOMER_ROUTE}?customer_id={CUSTOMER_TEST_API_LOGGED['id']}"
    response = requests.get(URL + route, headers=headers).json()

    assert response is not None
    assert response["email"] == CUSTOMER_TEST_API["email"]
    assert response["role"] == CUSTOMER_TEST_API["role"]
    assert response["full_name"] == CUSTOMER_TEST_API["full_name"]
    assert response["phone"] == CUSTOMER_TEST_API["phone"]
    assert response["address"] == CUSTOMER_TEST_API["address"]
    assert response["cpf_cnpj"] == CUSTOMER_TEST_API["cpf_cnpj"]
    assert response["id"] == CUSTOMER_TEST_API_LOGGED["id"]


def test_get_all_customers():
    """Test getting all customers returned by the API"""

    headers = {"Authorization": f"Bearer {TOKEN}"}
    customers = requests.get(URL + CUSTOMER_ROUTE, headers=headers).json()

    assert customers is not None
    assert len(customers) > 0

    customer = next(
        (
            customer
            for customer in customers
            if customer["id"] == CUSTOMER_TEST_API_LOGGED["id"]
        ),
        None,
    )

    assert customer is not None
    assert CUSTOMER_TEST_API_LOGGED["email"] == customer["email"]
    assert CUSTOMER_TEST_API_LOGGED["role"] == customer["role"]
    assert CUSTOMER_TEST_API_LOGGED["full_name"] == customer["full_name"]
    assert CUSTOMER_TEST_API_LOGGED["phone"] == customer["phone"]
    assert CUSTOMER_TEST_API_LOGGED["address"] == customer["address"]
    assert CUSTOMER_TEST_API_LOGGED["cpf_cnpj"] == customer["cpf_cnpj"]


def test_update_customer():
    """Test updating a customer by the API"""

    new_customer_data = {
        "full_name": fake.name(),
        "email": CUSTOMER_TEST_API_LOGGED["email"],
        "phone": generate_cell_phone_number(),
        "address": fake.address(),
        "cpf_cnpj": fake.random_element(elements=[generate_cpf(), generate_cnpj()]),
        "password_hash": generate_password(),
        "role": fake.random_element(elements=["customer", "admin"]),
    }

    headers = {"Authorization": f"Bearer {TOKEN}"}
    route = f"{CUSTOMER_ROUTE}?customer_id={CUSTOMER_TEST_API_LOGGED['id']}"
    response = requests.put(URL + route, json=new_customer_data, headers=headers).json()

    assert response is not None
    assert response == {"message": "Updated customer data successfully"}


def test_delete_customer():
    """Test deleting a customer by the API"""

    headers = {"Authorization": f"Bearer {TOKEN}"}
    route = f"{CUSTOMER_ROUTE}?customer_id={int(CUSTOMER_TEST_API_LOGGED['id'])}"
    response = requests.delete(URL + route, headers=headers).json()

    assert response is not None
    assert response == {"message": "Customer deleted successfully"}
