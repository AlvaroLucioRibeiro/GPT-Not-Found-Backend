from typing import Optional
from db.db_base_classes import OrderItem
from db.CRUD.create import create_order_item
from db.CRUD.update import update_order_item
from db.CRUD.delete import delete_order_item
from utils.utils_token_auth import get_current_user
from db.CRUD.read import get_order_item_by_id, get_order_items
from fastapi import APIRouter, HTTPException, Depends, Query, Body

order_items_router = APIRouter(prefix="/order_items", tags=["Order Items"])


@order_items_router.get("/")
async def list_order_items(
    order_item_id: Optional[int] = Query(None),
    current_user: dict = Depends(get_current_user),
):
    """
    Get a list of order items or a specific order item by ID.

    Args:
        order_item_id (Optional[int]): The ID of the order item to retrieve. If not provided, all order items are returned.
        current_user (dict): The current user making the request.

    Returns:
        List[OrderItem]: A list of order items or a single order item if ID is provided.

    HttpException:
        404: If the order item with the specified ID is not found.
        400: If there is an error retrieving the order items.
    """
    if order_item_id:
        item = await get_order_item_by_id(order_item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Order item not found")
        return item
    return await get_order_items()


@order_items_router.post("/")
async def create_new_order_item(
    item: OrderItem,
    current_user: dict = Depends(get_current_user),
):
    """
    Create a new order item.

    Args:
        item (OrderItem): The order item to create.
        current_user (dict): The current user making the request.

    Returns:
        dict: A message indicating the order item was created successfully.

    HttpException:
        400: If there is an error creating the order item.
    """
    try:
        return await create_order_item(item.dict())
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error creating order item: {str(e)}"
        )


@order_items_router.put("/")
async def modify_order_item(
    order_item_id: int = Query(...),
    item: OrderItem = Body(...),
    current_user: dict = Depends(get_current_user),
):
    """
    Update an existing order item.

    Args:
        order_item_id (int): The ID of the order item to update.
        item (OrderItem): The updated order item data.
        current_user (dict): The current user making the request.

    Returns:
        dict: A message indicating the order item was updated successfully.

    HttpException:
        404: If the order item with the specified ID is not found or update fails.
        400: If there is an error updating the order item.
    """
    updated_item = await update_order_item(order_item_id, item.dict())
    if not updated_item:
        raise HTTPException(
            status_code=404, detail="Order item not found or update failed"
        )
    return {"message": "Order item updated", "order_item": updated_item}


@order_items_router.delete("/")
async def remove_order_item(
    order_item_id: int = Query(...),
    current_user: dict = Depends(get_current_user),
):
    """
    Remove an order item.

    Args:
        order_item_id (int): The ID of the order item to remove.
        current_user (dict): The current user making the request.

    Returns:
        dict: A message indicating the order item was deleted successfully.

    HttpException:
        404: If the order item with the specified ID is not found or deletion fails.
        400: If there is an error deleting the order item.
    """
    success = await delete_order_item(order_item_id)
    if not success:
        raise HTTPException(
            status_code=404, detail="Order item not found or deletion failed"
        )
    return {"message": "Order item deleted"}
