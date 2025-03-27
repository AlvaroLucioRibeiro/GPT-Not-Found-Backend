import pytest
from datetime import datetime
from src.db.CRUD.read import get_payment_by_id
from src.db.CRUD.create import create_payment
from src.db.CRUD.update import update_payment

# Assuming that the order with ID 11 exists in the database
VALID_ORDER_ID = 11 

INVALID_PAYMENT_ID = 999999

PAYMENT_TEST_DATA = {
    "order_id": VALID_ORDER_ID,
    "amount": "2500.00",
    "payment_method": "pix",
    "status": "approved",
    "payment_date": datetime.now().isoformat()
}

CREATED_PAYMENT_ID = None

@pytest.mark.asyncio
async def test_create_payment_success():
    """Test creating a payment successfully"""
    global CREATED_PAYMENT_ID

    result = await create_payment(PAYMENT_TEST_DATA)
    assert result is not None
    assert "message" in result and result["message"] == "Payment created successfully!"
    assert "payment_id" in result

    CREATED_PAYMENT_ID = result["payment_id"]

@pytest.mark.asyncio
async def test_create_payment_failure():
    """Test creating a payment with missing required fields (should raise exception)"""
    with pytest.raises(Exception):
        await create_payment({})  # Dados vazios devem falhar

@pytest.mark.asyncio
async def test_get_payment_by_id_success():
    """Test retrieving a payment by valid ID"""
    payment = await get_payment_by_id(CREATED_PAYMENT_ID)
    assert payment is not None
    assert payment["id"] == CREATED_PAYMENT_ID
    assert payment["order_id"] == PAYMENT_TEST_DATA["order_id"]
    assert payment["amount"] == float(PAYMENT_TEST_DATA["amount"])
    assert payment["payment_method"] == PAYMENT_TEST_DATA["payment_method"]
    assert payment["status"] == PAYMENT_TEST_DATA["status"]

@pytest.mark.asyncio
async def test_get_payment_by_id_failure():
    """Test retrieving a payment with invalid ID"""
    payment = await get_payment_by_id(INVALID_PAYMENT_ID)
    assert payment is None

@pytest.mark.asyncio
async def test_update_payment_success():
    """Test updating a payment"""
    updated_data = {
        "amount": "3000.00",
        "payment_method": "credit_card",
        "status": "approved",
        "payment_date": datetime.now().isoformat()
    }

    result = await update_payment(CREATED_PAYMENT_ID, updated_data)
    assert result is not None
    assert result["message"] == "Payment successfully updated!"

    payment = result["payment"]
    assert payment[0] == CREATED_PAYMENT_ID
    assert str(payment[2]) == updated_data["amount"]
    assert payment[3] == updated_data["payment_method"]
    assert payment[4] == updated_data["status"]

@pytest.mark.asyncio
async def test_update_payment_failure():
    """Test updating a non-existing payment"""
    with pytest.raises(Exception):
        await update_payment(INVALID_PAYMENT_ID, {
            "amount": "9999.99",
            "payment_method": "boleto",
            "status": "pending",
            "payment_date": datetime.now().isoformat()
        })
