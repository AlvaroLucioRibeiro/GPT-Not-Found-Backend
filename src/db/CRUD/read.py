from fastapi import HTTPException
from typing import Dict, Optional, List
from db.db_sql_connection import connect


async def get_customer_by_email(email: str) -> Optional[Dict[str, str]]:
    """
    Recovery customer data by email

    Args:
        email (str): Customer email

    return:
        Optional[Dict[str, str]]: Customer data

    exceptions:
        HTTPException: Database error
    """
    query = "SELECT id, full_name, email, phone, address, cpf_cnpj, password_hash, role FROM customers WHERE email = %s;"

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (email,))
                customer = cursor.fetchone()

        if customer:
            return {
                "id": customer[0],
                "full_name": customer[1],
                "email": customer[2],
                "phone": customer[3],
                "address": customer[4],
                "cpf_cnpj": customer[5],
                "password_hash": customer[6],
                "role": customer[7],
            }
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_event_by_id(event_id: int) -> Optional[Dict[str, str]]:
    """
    Retrieves a specific event by its ID.

    Args:
        event_id (int): The event ID.

    Returns:
        Optional[Dict[str, str]]: Event details if found, otherwise None.

    Raises:
        HTTPException: If an error occurs while fetching the event.
    """
    query = "SELECT * FROM events WHERE id = %s;"

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (event_id,))
                row = cursor.fetchone()

                if row:
                    columns = [desc[0] for desc in cursor.description]
                    event = dict(zip(columns, row))
                    return event

        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_all_events() -> List[Dict[str, str]]:
    """
    Retrieves all events from the database.

    Returns:
        List[Dict[str, str]]: A list of dictionaries representing events.

    Raises:
        HTTPException: If an error occurs while fetching events.
    """
    query = """
        SELECT id, customer_id, event_type, event_date, location, guest_count, duration_hours, budget_approved 
        FROM events;
    """

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                columns = [desc[0] for desc in cursor.description]  # Get column names
                events = [
                    dict(zip(columns, row)) for row in cursor.fetchall()
                ]  # Convert rows to dictionaries
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
