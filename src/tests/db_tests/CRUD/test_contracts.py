import pytest
from faker import Faker
from src.db.CRUD.create import create_customer, create_event, create_contract
from src.db.CRUD.read import get_contract_by_event_id, get_contract_pdf
from src.db.CRUD.delete import delete_event, delete_customer
from src.tests.utils.utils import generate_random_email, generate_cpf, generate_password

fake = Faker()

CONTRACT_FILE_NAME = "test_contract_sample.pdf"
CUSTOMER_ID = None
EVENT_ID = None
CONTRACT_ID = None


@pytest.mark.asyncio
async def test_create_customer_for_contract():
    """Create a customer for linking to the event"""
    global CUSTOMER_ID

    customer_data = {
        "full_name": fake.name(),
        "email": generate_random_email(),
        "phone": fake.phone_number(),
        "address": fake.address(),
        "cpf_cnpj": generate_cpf(),
        "password_hash": generate_password(),
        "role": "customer",
    }

    response = await create_customer(customer_data)
    assert response is not None
    assert response["message"] == "Customer inserted successfully!"

    from src.db.CRUD.read import get_customer_by_email

    customer = await get_customer_by_email(customer_data["email"])
    assert customer is not None
    CUSTOMER_ID = customer["id"]


@pytest.mark.asyncio
async def test_create_event_for_contract():
    """Create event to associate with a contract"""
    global EVENT_ID

    event_data = {
        "customer_id": CUSTOMER_ID,
        "event_type": "wedding",
        "event_date": "2025-12-20 18:00:00",
        "location": "Praia do Futuro",
        "guest_count": 150,
        "duration_hours": 6,
        "budget_approved": True,
    }

    result = await create_event(event_data)
    assert result is not None
    assert result["message"] == "Event successfully created!"
    EVENT_ID = result["event_id"]


@pytest.mark.asyncio
async def test_create_contract():
    """Test contract creation linked to an event"""
    global CONTRACT_ID

    contract_data = {"event_id": EVENT_ID, "pdf_file": CONTRACT_FILE_NAME}

    result = await create_contract(contract_data)
    assert result is not None
    assert result["message"] == "Contract created successfully!"
    CONTRACT_ID = result["contract_id"]


@pytest.mark.asyncio
async def test_get_contract_by_event_id():
    """Test reading the contract by its event_id"""
    contract = await get_contract_by_event_id(EVENT_ID)
    assert contract is not None
    assert contract["event_id"] == EVENT_ID
    assert contract["pdf_file"] == CONTRACT_FILE_NAME


@pytest.mark.asyncio
async def test_get_contract_pdf():
    """Test fetching the PDF file name of the contract by contract_id"""
    pdf_data = await get_contract_pdf(CONTRACT_ID)
    assert pdf_data is not None
    assert pdf_data["pdf_file"] == CONTRACT_FILE_NAME


@pytest.mark.asyncio
async def test_cleanup_contract_event_and_customer():
    """Cleanup test by removing event and customer (contract removed via cascade)"""
    deleted_event = await delete_event(EVENT_ID)
    assert deleted_event is True

    deleted_customer = await delete_customer(CUSTOMER_ID)
    assert deleted_customer is True
