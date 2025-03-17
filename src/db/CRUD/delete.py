from fastapi import HTTPException
from db.db_sql_connection import connect


async def delete_event(event_id: int) -> bool:
    """
    Deletes an event from the database.

    Args:
        event_id (int): The event ID.

    Returns:
        bool: True if deletion was successful, False otherwise.

    Raises:
        HTTPException: If the deletion fails.
    """
    query = "DELETE FROM events WHERE id = %s RETURNING id;"

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (event_id,))
                deleted_event = cursor.fetchone()

            if not deleted_event:
                return False

            conn.commit()
        return True

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
