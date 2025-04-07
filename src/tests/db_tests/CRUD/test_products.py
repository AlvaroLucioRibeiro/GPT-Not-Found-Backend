import pytest
from faker import Faker
from src.db.CRUD.create import create_product
from src.db.CRUD.read import get_product_by_id, get_all_products
from src.db.CRUD.update import update_product
from src.db.CRUD.delete import delete_product

fake = Faker()

PRODUCT_TEST_DATA = {
    "name": fake.word().capitalize(),
    "description": fake.sentence(),
    "base_price": round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2),
    "category": fake.random_element(elements=["drink", "service", "structure"]),
    "active": True,
}

PRODUCT_ID_LOGGED = None


@pytest.mark.asyncio
async def test_create_product():
    """Test creating a new product"""
    global PRODUCT_ID_LOGGED

    result = await create_product(PRODUCT_TEST_DATA)
    assert result is not None
    assert "id" in result
    PRODUCT_ID_LOGGED = result["id"]

    # Verify inserted data
    assert result["name"] == PRODUCT_TEST_DATA["name"]
    assert result["description"] == PRODUCT_TEST_DATA["description"]
    assert float(result["base_price"]) == float(PRODUCT_TEST_DATA["base_price"])
    assert result["category"] == PRODUCT_TEST_DATA["category"]
    assert result["active"] == PRODUCT_TEST_DATA["active"]


@pytest.mark.asyncio
async def test_get_product_by_id():
    """Test fetching product by ID"""
    product = await get_product_by_id(PRODUCT_ID_LOGGED)
    assert product is not None
    assert product["id"] == PRODUCT_ID_LOGGED
    assert product["name"] == PRODUCT_TEST_DATA["name"]


@pytest.mark.asyncio
async def test_get_all_products():
    """Test fetching all products"""
    products = await get_all_products()
    assert products is not None
    assert isinstance(products, list)

    product = next((p for p in products if p["id"] == PRODUCT_ID_LOGGED), None)
    assert product is not None


@pytest.mark.asyncio
async def test_update_product():
    """Test updating a product"""
    updated_data = {
        "name": fake.word().capitalize(),
        "description": fake.text(max_nb_chars=50),
        "base_price": 99.99,
        "category": "structure",
        "active": False,
    }

    result = await update_product(PRODUCT_ID_LOGGED, updated_data)
    assert result is not None
    assert result["id"] == PRODUCT_ID_LOGGED
    assert result["name"] == updated_data["name"]
    assert result["active"] == updated_data["active"]


@pytest.mark.asyncio
async def test_delete_product():
    """Test deleting a product"""
    result = await delete_product(PRODUCT_ID_LOGGED)
    assert result is True

    # Check if product no longer exists
    product = await get_product_by_id(PRODUCT_ID_LOGGED)
    assert product is None
