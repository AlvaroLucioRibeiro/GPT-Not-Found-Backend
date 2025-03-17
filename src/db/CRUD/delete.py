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
