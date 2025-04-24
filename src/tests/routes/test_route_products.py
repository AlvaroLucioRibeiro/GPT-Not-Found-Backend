import requests
from faker import Faker
from src.tests.utils.utils import (
    generate_cell_phone_number,
    generate_cnpj,
    generate_cpf,
    generate_password,
    generate_random_email,
)

fake = Faker()

URL = "https://gpt-not-found.vercel.app"
LOGIN_ROUTE = "/auth/login"
CUSTOMER_ROUTE = "/customers"
PRODUCTS_ROUTE = "/products"

TOKEN = None
HEADERS = {}
CREATED_PRODUCT_ID = None
INVALID_PRODUCT_ID = 999999

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
    Test user authentication.

    This test registers a new user and authenticates them using their credentials.
    It checks whether the token is successfully returned and saved for future requests.
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


def test_create_product_success():
    """
    Test successful product creation.

    Sends a POST request to create a new product and checks if the product ID is returned.
    """
    global CREATED_PRODUCT_ID

    payload = {
        "name": "Gin Bar",
        "description": "Complete bar for gin drinks",
        "base_price": 1200.00,
        "category": "structure",
        "active": True,
    }

    response = requests.post(URL + PRODUCTS_ROUTE + "/", json=payload, headers=HEADERS)
    json_data = response.json()

    assert response.status_code == 200
    assert json_data["message"] == "Product created successfully!"
    CREATED_PRODUCT_ID = json_data["product"]["id"]


def test_get_product_by_valid_id():
    """
    Test fetching a product using a valid ID.

    Validates that the returned product matches the previously created product.
    """
    global CREATED_PRODUCT_ID

    response = requests.get(
        f"{URL + PRODUCTS_ROUTE}/?product_id={CREATED_PRODUCT_ID}", headers=HEADERS
    )

    assert response.status_code == 200
    assert response.json()["id"] == CREATED_PRODUCT_ID


def test_get_product_by_invalid_id():
    """
    Test fetching a product using an invalid ID.

    Expects a 404 response with the appropriate error message.
    """
    response = requests.get(
        f"{URL + PRODUCTS_ROUTE}/?product_id={INVALID_PRODUCT_ID}", headers=HEADERS
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_update_product():
    """
    Test updating an existing product.

    Sends a PUT request with new product data and checks if the update is acknowledged.
    """
    global CREATED_PRODUCT_ID

    payload = {
        "name": "Updated Bar",
        "description": "Updated description",
        "base_price": 1500.00,
        "category": "service",
        "active": False,
    }

    response = requests.put(
        f"{URL + PRODUCTS_ROUTE}/?product_id={CREATED_PRODUCT_ID}",
        json=payload,
        headers=HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Product updated successfully"


def test_delete_product():
    """
    Test deleting a previously created product.

    Sends a DELETE request and verifies that the product is removed successfully.
    """
    global CREATED_PRODUCT_ID

    response = requests.delete(
        f"{URL + PRODUCTS_ROUTE}/?product_id={CREATED_PRODUCT_ID}", headers=HEADERS
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Product deleted successfully"}
