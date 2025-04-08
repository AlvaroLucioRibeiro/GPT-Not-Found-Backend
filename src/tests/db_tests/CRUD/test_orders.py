import pytest
from faker import Faker
from datetime import datetime
from src.db.CRUD.create import create_order
from src.db.CRUD.read import get_order_by_id, get_all_orders
from src.db.CRUD.update import update_order
from src.db.CRUD.delete import delete_order

fake = Faker()

ORDER_TEST_DATA = {
    "event_id": 2001,
    "order_date": datetime.now().isoformat(),
    "total_amount": 4500.00,
    "status": "pending",
}

ORDER_ID_LOGGED = None


@pytest.mark.asyncio
async def test_create_order():
    """Test creating a new order"""
    global ORDER_ID_LOGGED

    result = await create_order(ORDER_TEST_DATA)
    assert result["message"] == "Order successfully created!"
    assert "order_id" in result

    ORDER_ID_LOGGED = result["order_id"]


@pytest.mark.asyncio
async def test_get_order_by_id():
    """Test fetching order by ID"""
    order = await get_order_by_id(ORDER_ID_LOGGED)
    assert order is not None
    assert order["id"] == ORDER_ID_LOGGED
    assert order["event_id"] == ORDER_TEST_DATA["event_id"]


@pytest.mark.asyncio
async def test_get_all_orders():
    """Test fetching all orders"""
    orders = await get_all_orders()
    assert orders is not None
    assert isinstance(orders, list)

    order = next((o for o in orders if o["id"] == ORDER_ID_LOGGED), None)
    assert order is not None


@pytest.mark.asyncio
async def test_update_order():
    """Test updating an order"""
    new_data = {
        "event_id": 2002,
        "order_date": datetime.now().isoformat(),
        "total_amount": 4999.99,
        "status": "paid",
    }

    result = await update_order(ORDER_ID_LOGGED, new_data)
    assert result["message"] == "Order successfully updated!"


@pytest.mark.asyncio
async def test_delete_order():
    """Test deleting an order"""
    result = await delete_order(ORDER_ID_LOGGED)
    assert result["message"] == "Order successfully deleted!"

    order = await get_order_by_id(ORDER_ID_LOGGED)
    assert order is None
