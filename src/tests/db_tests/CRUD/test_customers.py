import pytest
from faker import Faker
from src.db.CRUD.create import create_customer
from src.db.CRUD.update import update_customer
from src.db.CRUD.delete import delete_customer
from src.tests.utils.utils import generate_random_email, generate_cpf, generate_cnpj, generate_password
from src.db.CRUD.read import (
    get_customer_by_id,
    get_all_customers,
    get_customer_by_email,
)

fake = Faker()

CUSTOMER_TEST_DATA = {
    "full_name": fake.name(),
    "email": generate_random_email(),
    "phone": fake.phone_number(),
    "address": fake.address(),
    "cpf_cnpj": fake.random_element(elements=[generate_cpf(), generate_cnpj()]),
    "password_hash": generate_password(),
    "role": fake.random_element(elements=["customer", "admin"]),
}

CUSTOMER_TEST_DATA_LOGGED = None


@pytest.mark.asyncio
async def test_create_customer():
    """Test creating a new customer"""

    message = await create_customer(CUSTOMER_TEST_DATA)
    assert message is not None
    assert message == {"message": "Customer inserted successfully!"}


@pytest.mark.asyncio
async def test_get_customer_data_by_email():
    """Test getting a customer by email"""

    customer = await get_customer_by_email(CUSTOMER_TEST_DATA["email"])
    assert customer is not None

    # compare the data of the customer and the data that was inserted
    assert customer["full_name"] == CUSTOMER_TEST_DATA["full_name"]
    assert customer["email"] == CUSTOMER_TEST_DATA["email"]
    assert customer["phone"] == CUSTOMER_TEST_DATA["phone"]
    assert customer["address"] == CUSTOMER_TEST_DATA["address"]
    assert customer["cpf_cnpj"] == CUSTOMER_TEST_DATA["cpf_cnpj"]
    assert customer["password_hash"] == CUSTOMER_TEST_DATA["password_hash"]
    assert customer["role"] == CUSTOMER_TEST_DATA["role"]

    # defining customer data to be used in the next tests
    global CUSTOMER_TEST_DATA_LOGGED
    CUSTOMER_TEST_DATA_LOGGED = customer


@pytest.mark.asyncio
async def test_get_customer_by_id():
    """Test getting a customer by id"""

    customer = await get_customer_by_id(CUSTOMER_TEST_DATA_LOGGED["id"])
    assert customer is not None
    assert CUSTOMER_TEST_DATA_LOGGED["full_name"] == customer["full_name"]
    assert CUSTOMER_TEST_DATA_LOGGED["email"] == customer["email"]
    assert CUSTOMER_TEST_DATA_LOGGED["phone"] == customer["phone"]
    assert CUSTOMER_TEST_DATA_LOGGED["address"] == customer["address"]
    assert CUSTOMER_TEST_DATA_LOGGED["cpf_cnpj"] == customer["cpf_cnpj"]
    assert CUSTOMER_TEST_DATA_LOGGED["role"] == customer["role"]


@pytest.mark.asyncio
async def test_get_all_customers():
    """Test getting all customers"""

    customers = await get_all_customers()
    assert customers is not None
    assert len(customers) > 0

    # search for the customer that was inserted
    customer = next(
        (
            customer
            for customer in customers
            if customer["id"] == CUSTOMER_TEST_DATA_LOGGED["id"]
        ),
        None,
    )

    assert customer is not None
    assert CUSTOMER_TEST_DATA_LOGGED["full_name"] == customer["full_name"]
    assert CUSTOMER_TEST_DATA_LOGGED["email"] == customer["email"]
    assert CUSTOMER_TEST_DATA_LOGGED["phone"] == customer["phone"]
    assert CUSTOMER_TEST_DATA_LOGGED["address"] == customer["address"]
    assert CUSTOMER_TEST_DATA_LOGGED["cpf_cnpj"] == customer["cpf_cnpj"]
    assert CUSTOMER_TEST_DATA_LOGGED["role"] == customer["role"]


@pytest.mark.asyncio
async def test_update_customer():
    """Test updating a customer"""

    new_data = {
        "full_name": fake.name(),
        "email": generate_random_email(),
        "phone": fake.phone_number(),
        "address": fake.address(),
        "cpf_cnpj": fake.random_element(elements=[generate_cpf(), generate_cnpj()]),
        "password_hash": fake.sha256(),
        "role": fake.random_element(elements=["customer", "admin"]),
    }

    message = await update_customer(CUSTOMER_TEST_DATA_LOGGED["id"], new_data)

    # check if the message was returned correctly
    assert message is not None
    assert message["message"] == "Customer successfully updated!"

    # check if the data was updated correctly
    assert message["customer"] is not None
    assert message["customer"][0] == CUSTOMER_TEST_DATA_LOGGED["id"]
    assert message["customer"][1] == new_data["full_name"]
    assert message["customer"][2] == new_data["email"]
    assert message["customer"][3] == new_data["phone"]
    assert message["customer"][4] == new_data["address"]
    assert message["customer"][5] == new_data["cpf_cnpj"]
    assert message["customer"][6] == new_data["role"]


@pytest.mark.asyncio
async def test_delete_customer():
    """Test deleting a customer"""

    message = await delete_customer(CUSTOMER_TEST_DATA_LOGGED["id"])

    # check if the message was returned correctly
    assert message is not None
    assert message == True

    # check if the customer was deleted
    customer = await get_customer_by_id(CUSTOMER_TEST_DATA_LOGGED["id"])
    assert customer is None
