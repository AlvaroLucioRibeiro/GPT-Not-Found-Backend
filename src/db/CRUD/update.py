from typing import Dict
from fastapi import HTTPException
from db.db_sql_connection import connect


async def update_event(event_id: int, event_data: Dict[str, str]) -> Dict[str, str]:
    """
    Updates an existing event.

    Args:
        event_id (int): The event ID.
        event_data (Dict[str, str]): Updated event data.

    Returns:
        Dict[str, str]: Success message.

    Raises:
        HTTPException: If the update fails or the event is not found.
    """
    query = """
        UPDATE events
        SET event_type = %(event_type)s,
            event_date = %(event_date)s,
            location = %(location)s,
            guest_count = %(guest_count)s,
            duration_hours = %(duration_hours)s,
            budget_approved = %(budget_approved)s,
            updated_at = NOW()
        WHERE id = %(event_id)s
        RETURNING *;
    """

    # Add the event_id to the event_data dictionary
    event_data["event_id"] = event_id

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, event_data)
                updated_event = cursor.fetchone()

            if not updated_event:
                raise HTTPException(
                    status_code=404, detail="Event not found or update failed"
                )

            conn.commit()
        return {"message": "Event successfully updated!", "event": updated_event}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
