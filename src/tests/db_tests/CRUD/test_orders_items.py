import pytest
from faker import Faker
from datetime import datetime
from src.db.CRUD.create import create_order, create_order_item
from src.db.CRUD.update import update_order_item
from src.db.CRUD.delete import delete_order_item
from src.db.CRUD.read import get_order_item_by_id, get_order_items, get_product_by_id


fake = Faker()

ORDER_ID_LOGGED = None
ORDER_ITEM_ID_LOGGED = None
PRODUCT_ID_LOGGED = None

ORDER_TEST_DATA = {
    "event_id": 2001,
    "order_date": datetime.now().isoformat(),
    "total_amount": 4500.00,
    "status": "pending",
}


@pytest.mark.asyncio
async def test_create_order_item():
    global ORDER_ID_LOGGED, ORDER_ITEM_ID_LOGGED, PRODUCT_ID_LOGGED

    # Criar pedido
    order_result = await create_order(ORDER_TEST_DATA)
    assert order_result["message"] == "Order successfully created!"
    ORDER_ID_LOGGED = order_result["order_id"]

    # Usar produto existente
    product = await get_product_by_id(4002)
    assert product is not None and product["active"] is True
    PRODUCT_ID_LOGGED = product["id"]

    unit_price = float(product["base_price"])
    quantity = 2
    total_price = quantity * unit_price

    order_item_data = {
        "order_id": ORDER_ID_LOGGED,
        "product_id": PRODUCT_ID_LOGGED,
        "quantity": quantity,
        "unit_price": unit_price,
        "total_price": total_price,
    }

    result = await create_order_item(order_item_data)
    assert result["message"] == "Order item created"
    assert "order_item_id" in result

    ORDER_ITEM_ID_LOGGED = result["order_item_id"]


@pytest.mark.asyncio
async def test_get_order_item_by_id():
    item = await get_order_item_by_id(ORDER_ITEM_ID_LOGGED)
    assert item is not None
    assert item["id"] == ORDER_ITEM_ID_LOGGED


@pytest.mark.asyncio
async def test_get_order_items():
    items = await get_order_items()
    assert isinstance(items, list)

    item = next((i for i in items if i["id"] == ORDER_ITEM_ID_LOGGED), None)
    assert item is not None


@pytest.mark.asyncio
async def test_update_order_item():
    new_data = {
        "order_id": ORDER_ID_LOGGED,
        "product_id": PRODUCT_ID_LOGGED,
        "quantity": 3,
        "unit_price": 99.99,
        "total_price": round(3 * 99.99, 2),
    }

    result = await update_order_item(ORDER_ITEM_ID_LOGGED, new_data)
    assert result is not None
    assert result["quantity"] == 3


@pytest.mark.asyncio
async def test_delete_order_item():
    result = await delete_order_item(ORDER_ITEM_ID_LOGGED)
    assert result is True

    item = await get_order_item_by_id(ORDER_ITEM_ID_LOGGED)
    assert item is None
