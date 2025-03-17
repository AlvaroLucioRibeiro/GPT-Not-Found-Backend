from typing import Dict
from fastapi import HTTPException
from db.db_sql_connection import connect


async def create_customer(customer_data: Dict[str, str]) -> Dict[str, str]:
    """
    Insert a new customer into the customers table.

    Args:
        customer_data (Dict[str, str]): Dictionary with customer data.

    Returns:
        Dict[str, str]: Message confirming the customer was inserted.

    Raises:
        HTTPException: If an error occurs while trying to insert the customer.
    """
    query = """
        INSERT INTO customers (full_name, email, phone, address, cpf_cnpj, password_hash, role)
        VALUES (%(full_name)s, %(email)s, %(phone)s, %(address)s, %(cpf_cnpj)s, %(password_hash)s, %(role)s);
    """

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, customer_data)
            conn.commit()
        return {"message": "Customer inserted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def create_event(event_data: Dict[str, str]) -> Dict[str, str]:
    """
    Inserts a new event into the 'events' table.

    Args:
        event_data (Dict[str, str]): Dictionary containing the event details.

    Returns:
        Dict[str, str]: Success message.

    Raises:
        HTTPException: If an error occurs while inserting the event into the database.
    """
    query = """
        INSERT INTO events (customer_id, event_type, event_date, location, guest_count, duration_hours, budget_approved)
        VALUES (%(customer_id)s, %(event_type)s, %(event_date)s, %(location)s, %(guest_count)s, %(duration_hours)s, %(budget_approved)s);
    """

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, event_data)
            conn.commit()
        return {"message": "Event successfully created!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
