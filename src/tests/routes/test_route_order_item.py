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
PRODUCTS_ROUTE = "/products"
ORDER_ITEMS_ROUTE = "/order_items"

TOKEN = None
HEADERS = {}
CREATED_ORDER_ID = None
CREATED_PRODUCT_ID = None
CREATED_ORDER_ITEM_ID = None

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


def test_create_order_item_dependencies():
    global CREATED_ORDER_ID, CREATED_PRODUCT_ID

    order_payload = {
        "event_id": 2001,
        "total_amount": 5000.00,
        "status": "pending",
    }
    order_resp = requests.post(URL + ORDERS_ROUTE + "/", json=order_payload, headers=HEADERS)
    assert order_resp.status_code == 200
    CREATED_ORDER_ID = order_resp.json()["order"]["order_id"]

    product_payload = {
        "name": fake.word(),
        "description": fake.sentence(),
        "category": "service",
        "base_price": 25.00,
        "active": True,
    }
    product_resp = requests.post(URL + PRODUCTS_ROUTE + "/", json=product_payload, headers=HEADERS)
    assert product_resp.status_code == 200
    CREATED_PRODUCT_ID = product_resp.json()["product"]["id"]


def test_create_order_item_success():
    global CREATED_ORDER_ITEM_ID

    payload = {
        "order_id": CREATED_ORDER_ID,
        "product_id": CREATED_PRODUCT_ID,
        "quantity": 2,
    }

    response = requests.post(URL + ORDER_ITEMS_ROUTE + "/", json=payload, headers=HEADERS)
    json_data = response.json()

    assert response.status_code == 200
    assert json_data["message"] == "Order item created"
    CREATED_ORDER_ITEM_ID = json_data["order_item_id"]


def test_get_order_item_by_valid_id():
    assert CREATED_ORDER_ITEM_ID is not None

    response = requests.get(
        f"{URL + ORDER_ITEMS_ROUTE}/?order_item_id={CREATED_ORDER_ITEM_ID}",
        headers=HEADERS,
    )
    assert response.status_code == 200
    assert response.json()["id"] == CREATED_ORDER_ITEM_ID


def test_update_order_item_success():
    assert CREATED_ORDER_ITEM_ID is not None

    payload = {
        "order_id": CREATED_ORDER_ID,
        "product_id": CREATED_PRODUCT_ID,
        "quantity": 150,
        "unit_price": 25.00,
        "total_price": 3750.00,
    }

    response = requests.put(
        f"{URL + ORDER_ITEMS_ROUTE}/?order_item_id={CREATED_ORDER_ITEM_ID}",
        json=payload,
        headers=HEADERS,
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Order item updated"


def test_delete_order_item_success():
    assert CREATED_ORDER_ITEM_ID is not None

    response = requests.delete(
        f"{URL + ORDER_ITEMS_ROUTE}/?order_item_id={CREATED_ORDER_ITEM_ID}",
        headers=HEADERS,
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Order item deleted"}
