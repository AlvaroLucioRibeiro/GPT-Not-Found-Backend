from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends, Query, Body
from db.CRUD.create import create_order
from db.CRUD.read import get_order_by_id, get_all_orders
from db.CRUD.update import update_order
from db.CRUD.delete import delete_order
from utils.utils_token_auth import get_current_user
from db.db_base_classes import Order

orders_router = APIRouter(prefix="/orders", tags=["Orders"])


@orders_router.get("/")
async def get_orders(
    order_id: Optional[int] = Query(None, description="The order identifier"),
    current_user: dict = Depends(get_current_user),
):
    """
    Retrieves all orders or a specific order if 'order_id' is provided.

    Args:
        order_id (Optional[int]): The order identifier (query parameter).
        current_user (dict): The authenticated user.

    Returns:
        dict or list: Order details if 'order_id' is provided, otherwise a list of all orders.

    Raises:
        HTTPException: If the order is not found.
    """
    if order_id:
        order = await get_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    return await get_all_orders()


@orders_router.post("/")
async def create_new_order(
    order: Order, current_user: dict = Depends(get_current_user)
):
    """
    Creates a new order.

    Args:
        order (Order): The order details.
        current_user (dict): The authenticated user.

    Returns:
        dict: Message confirming order creation.

    Raises:
        HTTPException: If the order creation fails.
    """
    try:
        order_data = order.dict()
        new_order = await create_order(order_data)
        return {"message": "Order created successfully!", "order": new_order}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating order: {str(exc)}",
        )


@orders_router.put("/")
async def modify_order(
    order_id: int = Query(..., description="The order identifier"),
    order: Order = Body(...),
    current_user: dict = Depends(get_current_user),
):
    """
    Updates an existing order using a query parameter for 'order_id' and request body for order data.

    Args:
        order_id (int): The order identifier (query parameter).
        order (Order): The updated order data from request body.
        current_user (dict): The authenticated user.

    Returns:
        dict: Updated order details.

    Raises:
        HTTPException: If the update fails.
    """
    existing_order = await get_order_by_id(order_id)

    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")

    updated_order = await update_order(order_id, order.dict())

    if not updated_order:
        raise HTTPException(status_code=500, detail="Order update failed")

    return {"message": "Order updated successfully", "order": updated_order}


@orders_router.delete("/")
async def remove_order(
    order_id: int = Query(..., description="The order identifier"),
    current_user: dict = Depends(get_current_user),
):
    """
    Deletes an order using a query parameter for 'order_id'.

    Args:
        order_id (int): The order identifier (query parameter).
        current_user (dict): The authenticated user.

    Returns:
        dict: Confirmation message.

    Raises:
        HTTPException: If the order is not found or deletion fails.
    """
    existing_order = await get_order_by_id(order_id)

    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")

    deleted = await delete_order(order_id)

    if not deleted:
        raise HTTPException(status_code=500, detail="Order could not be deleted")

    return {"message": "Order deleted successfully"}
