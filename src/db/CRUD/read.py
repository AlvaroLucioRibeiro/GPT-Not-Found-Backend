from typing import Dict, List, Optional
from fastapi import HTTPException
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


async def get_order_by_id(order_id: int) -> Optional[Dict[str, str]]:
    """
    Retrieves an order by its ID.

    Args:
        order_id (int): The order identifier.

    Returns:
        Optional[Dict[str, str]]: Order details if found, otherwise None.

    Raises:
        HTTPException: If an error occurs while fetching data from the database.
    """
    query = "SELECT * FROM orders WHERE id = %(order_id)s"
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, {"order_id": order_id})
                order = cursor.fetchone()
        return order if order else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_all_orders() -> List[Dict[str, str]]:
    """
    Retrieves all registered orders.

    Returns:
        List[Dict[str, str]]: List containing all orders.

    Raises:
        HTTPException: If an error occurs while fetching data from the database.
    """
    query = "SELECT * FROM orders"
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                orders = cursor.fetchall()
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
