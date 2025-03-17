from typing import Optional
from db.db_base_classes import Event
from db.CRUD.create import create_event
from db.CRUD.update import update_event
from db.CRUD.delete import delete_event
from utils.utils_token_auth import get_current_user
from db.CRUD.read import get_event_by_id, get_all_events
from fastapi import APIRouter, HTTPException, status, Depends, Query, Body

events_router = APIRouter(prefix="/events", tags=["Events"])


@events_router.get("/")
async def get_events(
    event_id: Optional[int] = Query(None, description="The event identifier"),
    current_user: dict = Depends(get_current_user),
):
    """
    Retrieves all events or a specific event if 'event_id' is provided.

    Args:
        event_id (Optional[int]): The event identifier (query parameter).
        current_user (dict): The authenticated user.

    Returns:
        dict or list: Event details if 'event_id' is provided, otherwise a list of all events.

    Raises:
        HTTPException: If the event is not found.
    """
    if event_id:  # if event_id is provided, return the event details
        event = await get_event_by_id(event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return event

    # if no event_id is provided, return all events
    return await get_all_events()


@events_router.post("/")
async def create_new_event(
    event: Event, current_user: dict = Depends(get_current_user)
):
    """
    Creates a new event.

    Args:
        event (Event): The event details.
        current_user (dict): The authenticated user.

    Returns:
        dict: Message confirming event creation.

    Raises:
        HTTPException: If the event creation fails.
    """
    try:
        event.customer_id = current_user["id"]
        new_event = await create_event(event.dict())
        return {"message": "Event created successfully!", "event": new_event}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating event: {str(exc)}",
        )


@events_router.put("/")
async def modify_event(
    event_id: int = Query(..., description="The event identifier"),
    event: Event = Body(...),
    current_user: dict = Depends(get_current_user),
):
    """
    Updates an existing event using a query parameter for 'event_id' and request body for event data.

    Args:
        event_id (int): The event identifier (query parameter).
        event (Event): The updated event data from request body.
        current_user (dict): The authenticated user.

    Returns:
        dict: Updated event details.

    Raises:
        HTTPException: If the update fails.
    """
    # search for the event in the database before updating
    existing_event = await get_event_by_id(event_id)

    if not existing_event:
        raise HTTPException(status_code=404, detail="Event not found")

    # take the customer_id from the existing event (in case permission checks are needed later)
    customer_id = existing_event["customer_id"]

    # Update the event
    event_data = event.dict()
    event_data["customer_id"] = customer_id  # add the customer_id to the event data

    updated_event = await update_event(event_id, event_data)

    if not updated_event:
        raise HTTPException(status_code=500, detail="Event update failed")

    return {"message": "Event updated successfully", "event": updated_event}


@events_router.delete("/")
async def remove_event(
    event_id: int = Query(..., description="The event identifier"),
    current_user: dict = Depends(get_current_user),
):
    """
    Deletes an event using a query parameter for 'event_id'.

    Args:
        event_id (int): The event identifier (query parameter).
        current_user (dict): The authenticated user.

    Returns:
        dict: Confirmation message.

    Raises:
        HTTPException: If the event is not found or deletion fails.
    """
    # search for the event in the database before deleting
    existing_event = await get_event_by_id(event_id)

    if not existing_event:
        raise HTTPException(status_code=404, detail="Event not found")

    # take the customer_id from the existing event (in case permission checks are needed later)
    customer_id = existing_event["customer_id"]

    # Delete the event
    deleted = await delete_event(event_id)

    if not deleted:
        raise HTTPException(status_code=500, detail="Event could not be deleted")

    return {"message": "Event deleted successfully"}
