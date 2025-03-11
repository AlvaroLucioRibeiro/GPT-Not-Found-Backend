from fastapi import APIRouter, HTTPException, status
from db.db_base_classes import Customer
from db.CRUD.create import create_customer
from utils.utils_validation import (
    get_password_hash,
    validate_password_strength,
    validate_email_format,
)

# -------------------- Authentication ROUTES -------------------- #

authentication_router = APIRouter(prefix="/auth", tags=["Authentication"])


@authentication_router.post("/register")
async def register(customer: Customer):
    """
    Registers a new user in the system.

    Args:
        customer (Customer): Object containing the user information to be registered.

    Returns:
        dict: Message confirming the successful user registration.

    Raises:
        HTTPException: Raised in case of email validation failure,
                       weak password, or unexpected registration errors.
    """

    try:
        # Validate email format
        validate_email_format(customer.email)

        # Validate password strength
        validate_password_strength(customer.password_hash)

        # Hash the password before storing it in the database
        customer.password_hash = get_password_hash(customer.password_hash)

        # Create the user in the database
        await create_customer(customer.dict())

        return {"message": f"User {customer.full_name} registered successfully!"}

    except ValueError as val_exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(val_exc)
        )

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error registering user: {str(exc)}",
        )
