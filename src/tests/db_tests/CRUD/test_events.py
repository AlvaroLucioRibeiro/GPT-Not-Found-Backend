import pytest
from datetime import datetime
from src.db.CRUD.create import create_event
from src.db.CRUD.read import get_event_by_id
from src.db.CRUD.update import update_event
from src.db.CRUD.delete import delete_event

EXISTING_EVENT_ID = 2005
INVALID_EVENT_ID = 999999
CREATED_EVENT_ID = None

BASE_EVENT_DATA = {
    "customer_id": 1005,
    "event_type": "wedding",  # updated in test_update_event_success
    "event_date": "2025-10-10T17:00:00",
    "location": "Sítio Paraíso",  # changed by update test
    "guest_count": 250,
    "duration_hours": 7,
    "budget_approved": True,
}


@pytest.mark.asyncio
async def test_create_event_success():
    """Test creating a new event successfully"""
    global CREATED_EVENT_ID

    new_event = {
        "customer_id": 1001,
        "event_type": "debutante",
        "event_date": "2025-12-25T20:00:00",
        "location": "Espaço Tropical",
        "guest_count": 100,
        "duration_hours": 4,
        "budget_approved": True,
    }

    result = await create_event(new_event)
    assert result is not None
    assert result["message"] == "Event successfully created!"
    assert "event_id" in result

    CREATED_EVENT_ID = result["event_id"]

    event = await get_event_by_id(CREATED_EVENT_ID)
    assert event is not None
    assert event["location"] == new_event["location"]
    assert event["event_type"] == new_event["event_type"]


@pytest.mark.asyncio
async def test_create_event_missing_field_failure():
    """Test creating an event with missing required fields"""
    with pytest.raises(Exception):
        await create_event({
            "customer_id": 1001,
            "event_type": "corporate"
        })


@pytest.mark.asyncio
async def test_create_event_invalid_enum_failure():
    """Test creating an event with an invalid enum value"""
    with pytest.raises(Exception):
        await create_event({
            "customer_id": 1002,
            "event_type": "birthday",  # invalid enum
            "event_date": "2025-12-30T21:00:00",
            "location": "Invalid Venue",
            "guest_count": 50,
            "duration_hours": 3,
            "budget_approved": False,
        })


@pytest.mark.asyncio
async def test_get_event_by_id_success():
    """Test retrieving an event by a valid ID"""
    event = await get_event_by_id(EXISTING_EVENT_ID)
    assert event is not None
    assert event["id"] == EXISTING_EVENT_ID
    assert event["customer_id"] == BASE_EVENT_DATA["customer_id"]
    assert event["event_type"] == BASE_EVENT_DATA["event_type"]
    assert event["location"] == BASE_EVENT_DATA["location"]
    assert event["guest_count"] == BASE_EVENT_DATA["guest_count"]
    assert event["duration_hours"] == BASE_EVENT_DATA["duration_hours"]


@pytest.mark.asyncio
async def test_get_event_by_id_failure():
    """Test retrieving an event by an invalid ID"""
    event = await get_event_by_id(INVALID_EVENT_ID)
    assert event is None


@pytest.mark.asyncio
async def test_update_event_success():
    """Test updating an existing event"""
    updated_data = {
        "event_type": "wedding",
        "event_date": "2025-11-11T19:00:00",
        "location": "Sítio Paraíso",
        "guest_count": 250,
        "duration_hours": 7,
        "budget_approved": True,
    }

    result = await update_event(EXISTING_EVENT_ID, updated_data)
    assert result["message"] == "Event successfully updated!"

    event = await get_event_by_id(EXISTING_EVENT_ID)
    assert event["event_type"] == updated_data["event_type"]
    assert event["location"] == updated_data["location"]
    assert event["guest_count"] == updated_data["guest_count"]
    assert event["duration_hours"] == updated_data["duration_hours"]
    assert event["budget_approved"] == updated_data["budget_approved"]


@pytest.mark.asyncio
async def test_update_event_failure():
    """Test updating a non-existing event"""
    with pytest.raises(Exception):
        await update_event(INVALID_EVENT_ID, {
            "event_type": "other",
            "event_date": "2025-12-01T20:00:00",
            "location": "Espaço Inexistente",
            "guest_count": 50,
            "duration_hours": 2,
            "budget_approved": False,
        })


@pytest.mark.asyncio
async def test_delete_event_success():
    """Test deleting a previously created event"""
    global CREATED_EVENT_ID
    assert CREATED_EVENT_ID is not None, "No created event ID found."

    result = await delete_event(CREATED_EVENT_ID)
    assert result is True

    deleted_event = await get_event_by_id(CREATED_EVENT_ID)
    assert deleted_event is None


@pytest.mark.asyncio
async def test_delete_event_failure():
    """Test deleting a non-existing event"""
    result = await delete_event(INVALID_EVENT_ID)
    assert result is False
