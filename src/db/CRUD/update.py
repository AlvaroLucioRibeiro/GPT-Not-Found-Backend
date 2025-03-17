from typing import Dict
from fastapi import HTTPException
from db.db_sql_connection import connect


async def update_order(order_id: int, order_data: Dict[str, str]) -> Dict[str, str]:
    """
    Updates an existing order in the orders table.

    Args:
        order_id (int): The order identifier.
        order_data (Dict[str, str]): Updated order details.

    Returns:
        Dict[str, str]: Success or error message.

    Raises:
        HTTPException: If an error occurs while updating data in the database.
    """
    query = """
        UPDATE orders
        SET event_id = %(event_id)s, order_date = %(order_date)s, total_amount = %(total_amount)s, status = %(status)s
        WHERE id = %(order_id)s;
    """
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, {"order_id": order_id, **order_data})
            conn.commit()
        return {"message": "Order successfully updated!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
