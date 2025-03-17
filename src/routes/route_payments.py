from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends, Query, Body
from db.db_base_classes import Payment
from db.CRUD.create import create_payment
from db.CRUD.read import get_payment_by_id
from db.CRUD.update import update_payment
from utils.utils_token_auth import get_current_user

payments_router = APIRouter(prefix="/payments", tags=["Payments"])


@payments_router.post("/")
async def create_new_payment(
    payment: Payment, current_user: dict = Depends(get_current_user)
):
    """
    Creates a new payment.

    Args:
        payment (Payment): The payment details.
        current_user (dict): The authenticated user.

    Returns:
        dict: Message confirming payment creation.

    Raises:
        HTTPException: If the payment creation fails.
    """
    try:
        payment_data = payment.dict()
        new_payment = await create_payment(payment_data)
        return {"message": "Payment created successfully!", "payment": new_payment}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating payment: {str(exc)}",
        )


@payments_router.get("/")
async def get_payment(
    payment_id: int,
    current_user: dict = Depends(get_current_user),
):
    """
    Retrieves a payment by its ID.

    Args:
        payment_id (int): The payment identifier.
        current_user (dict): The authenticated user.

    Returns:
        dict: Payment details.

    Raises:
        HTTPException: If the payment is not found.
    """
    payment = await get_payment_by_id(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@payments_router.put("/")
async def modify_payment(
    payment_id: int = Query(..., description="The payment identifier"),
    payment: Payment = Body(...),
    current_user: dict = Depends(get_current_user),
):
    """
    Updates an existing payment using a query parameter for 'payment_id' and request body for payment data.

    Args:
        payment_id (int): The payment identifier (query parameter).
        payment (Payment): The updated payment data from request body.
        current_user (dict): The authenticated user.

    Returns:
        dict: Updated payment details.

    Raises:
        HTTPException: If the update fails.
    """
    existing_payment = await update_payment(payment_id, payment.dict())

    if not existing_payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    return {"message": "Payment updated successfully", "payment": existing_payment}
