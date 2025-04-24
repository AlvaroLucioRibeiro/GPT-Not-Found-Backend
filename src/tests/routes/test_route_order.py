import requests
from faker import Faker
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
ORDERS_ROUTE = "/orders"

TOKEN = None
HEADERS = {}
CREATED_ORDER_ID = None
INVALID_ORDER_ID = 999999

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
    Test user authentication and save the token for future requests.
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


def test_create_order_success():
    """
    Test creating an order successfully.
    """
    global CREATED_ORDER_ID

    payload = {
        "event_id": 2001,
        "total_amount": 4500.00,
        "status": "pending",
    }

    response = requests.post(URL + ORDERS_ROUTE + "/", json=payload, headers=HEADERS)
    json_data = response.json()

    assert response.status_code == 200
    assert json_data["message"] == "Order created successfully!"
    CREATED_ORDER_ID = json_data["order"]["order_id"]  # ✅ Corrigido aqui


def test_get_order_by_valid_id():
    """
    Test fetching an order using a valid ID.
    """
    global CREATED_ORDER_ID

    response = requests.get(
        f"{URL + ORDERS_ROUTE}/?order_id={CREATED_ORDER_ID}",
        headers=HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["id"] == CREATED_ORDER_ID


def test_get_order_by_invalid_id():
    """
    Test fetching an order using an invalid ID.
    """
    response = requests.get(
        f"{URL + ORDERS_ROUTE}/?order_id={INVALID_ORDER_ID}",
        headers=HEADERS,
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}


def test_update_order_success():
    """
    Test updating an existing order.
    """
    global CREATED_ORDER_ID

    payload = {
        "event_id": 2002,
        "total_amount": 5999.99,
        "status": "paid",
    }

    response = requests.put(
        f"{URL + ORDERS_ROUTE}/?order_id={CREATED_ORDER_ID}",
        json=payload,
        headers=HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Order updated successfully"


def test_delete_order_success():
    """
    Test deleting an existing order.
    """
    global CREATED_ORDER_ID

    response = requests.delete(
        f"{URL + ORDERS_ROUTE}/?order_id={CREATED_ORDER_ID}",
        headers=HEADERS,
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Order deleted successfully"}
