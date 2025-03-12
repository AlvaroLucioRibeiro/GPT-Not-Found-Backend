from fastapi import APIRouter, Depends
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
