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


@payments_router.get("/{payment_id}")
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


@payments_router.put("/{payment_id}")
async def modify_payment(
    payment_id: int,
    payment: Payment = Body(...),
    current_user: dict = Depends(get_current_user),
):
    """
    Updates an existing payment.

    Args:
        payment_id (int): The payment identifier.
        payment (Payment): The updated payment data.
        current_user (dict): The authenticated user.

    Returns:
        dict: Updated payment details.

    Raises:
        HTTPException: If the update fails.
    """
    existing_payment = await get_payment_by_id(payment_id)

    if not existing_payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    updated_payment = await update_payment(payment_id, payment.dict())

    if not updated_payment:
        raise HTTPException(status_code=500, detail="Payment update failed")

    return {"message": "Payment updated successfully", "payment": updated_payment}
