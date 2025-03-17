from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends, Query, Body
from db.db_base_classes import Customer
from db.CRUD.create import create_customer
from db.CRUD.read import get_customer_by_id, get_all_customers
from db.CRUD.update import update_customer
from db.CRUD.delete import delete_customer
from utils.utils_token_auth import get_current_user

customers_router = APIRouter(prefix="/customers", tags=["Customers"])


@customers_router.get("/me")
async def get_my_data(current_user: dict = Depends(get_current_user)):
    """
    Returns the authenticated user's data.

    Args:
        current_user (dict): The authenticated user.

    Returns:
        dict: The authenticated user's information.
    """
    return {"user": current_user}


@customers_router.get("/")
async def get_customers(
    customer_id: Optional[int] = Query(None, description="The customer identifier"),
    current_user: dict = Depends(get_current_user),
):
    """
    Retrieves all customers or a specific customer if 'customer_id' is provided.

    Args:
        customer_id (Optional[int]): The customer identifier (query parameter).
        current_user (dict): The authenticated user.

    Returns:
        dict or list: Customer details if 'customer_id' is provided, otherwise a list of all customers.

    Raises:
        HTTPException: If the customer is not found.
    """
    if customer_id:
        customer = await get_customer_by_id(customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer

    return await get_all_customers()


@customers_router.post("/")
async def create_new_customer(
    customer: Customer,
):
    """
    Creates a new customer.

    Args:
        customer (Customer): The customer details.

    Returns:
        dict: Message confirming customer creation.

    Raises:
        HTTPException: If the customer creation fails.
    """
    try:
        customer_data = customer.dict()
        new_customer = await create_customer(customer_data)
        return {"message": "Customer created successfully!", "customer": new_customer}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating customer: {str(exc)}",
        )


@customers_router.put("/")
async def modify_customer(
    customer_id: int = Query(..., description="The customer identifier"),
    customer: Customer = Body(...),
    current_user: dict = Depends(get_current_user),
):
    """
    Updates an existing customer using a query parameter for 'customer_id' and request body for customer data.

    Args:
        customer_id (int): The customer identifier (query parameter).
        customer (Customer): The updated customer data from request body.
        current_user (dict): The authenticated user.

    Returns:
        dict: Updated customer details.

    Raises:
        HTTPException: If the update fails.
    """
    existing_customer = await get_customer_by_id(customer_id)

    if not existing_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    updated_customer = await update_customer(customer_id, customer.dict())

    if not updated_customer:
        raise HTTPException(status_code=500, detail="Customer update failed")

    return {"message": "Customer updated successfully", "customer": updated_customer}


@customers_router.delete("/")
async def remove_customer(
    customer_id: int = Query(..., description="The customer identifier"),
    current_user: dict = Depends(get_current_user),
):
    """
    Deletes a customer using a query parameter for 'customer_id'.

    Args:
        customer_id (int): The customer identifier (query parameter).
        current_user (dict): The authenticated user.

    Returns:
        dict: Confirmation message.

    Raises:
        HTTPException: If the customer is not found or deletion fails.
    """
    existing_customer = await get_customer_by_id(customer_id)

    if not existing_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    deleted = await delete_customer(customer_id)

    if not deleted:
        raise HTTPException(status_code=500, detail="Customer could not be deleted")

    return {"message": "Customer deleted successfully"}
