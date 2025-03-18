from typing import Dict
from fastapi import HTTPException
from db.db_sql_connection import connect


async def delete_order(order_id: int) -> Dict[str, str]:
    """
    Removes an order from the orders table.

    Args:
        order_id (int): The order identifier.

    Returns:
        Dict[str, str]: Success or error message.

    Raises:
        HTTPException: If an error occurs while deleting data from the database.
    """
    query = "DELETE FROM orders WHERE id = %(order_id)s"
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, {"order_id": order_id})
            conn.commit()
        return {"message": "Order successfully deleted!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


async def delete_customer(customer_id: int) -> bool:
    """
    Deletes a customer from the database.

    Args:
        customer_id (int): The customer ID.

    Returns:
        bool: True if deletion was successful, False otherwise.

    Raises:
        HTTPException: If the deletion fails.
    """
    query = "DELETE FROM customers WHERE id = %s RETURNING id;"

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (customer_id,))
                deleted_customer = cursor.fetchone()

            if not deleted_customer:
                return False  # Customer not found

            conn.commit()
        return True  # Customer deleted successfully

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def delete_product(product_id: int) -> bool:
    """
    Deletes a product from the database.

    Args:
        product_id (int): The product ID.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    query = "DELETE FROM products WHERE id = %s RETURNING id;"
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (product_id,))
                deleted_product = cursor.fetchone()
                if not deleted_product:
                    return False
                conn.commit()
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
