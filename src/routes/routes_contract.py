from fastapi import APIRouter, HTTPException, status, Depends
from db.CRUD.read import get_contract_by_event_id, get_contract_pdf
from db.CRUD.create import create_contract
from db.db_base_classes import Contract
from utils.utils_token_auth import get_current_user

contracts_router = APIRouter(prefix="/contracts", tags=["Contracts"])


@contracts_router.post("/")
async def create_new_contract(
    contract: Contract, current_user: dict = Depends(get_current_user)
):
    """
    Creates a new contract.

    Args:
        contract (Contract): The contract details.
        current_user (dict): The authenticated user.

    Returns:
        dict: Success message and contract ID.

    Raises:
        HTTPException: If the contract creation fails.
    """
    try:
        contract_data = contract.dict()
        new_contract = await create_contract(contract_data)
        return new_contract
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating contract: {str(exc)}",
        )


@contracts_router.get("/")
async def get_contract(
    event_id: int,
    current_user: dict = Depends(get_current_user),
):
    """
    Retrieves contracts related to a specific event.

    Args:
        event_id (int): The event ID to fetch contracts for.
        current_user (dict): The authenticated user.

    Returns:
        dict: Contract details.

    Raises:
        HTTPException: If the contract is not found.
    """
    contract = await get_contract_by_event_id(event_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    return contract


@contracts_router.get("/download/")
async def download_contract(
    contract_id: int,
    current_user: dict = Depends(get_current_user),
):
    """
    Retrieves the PDF file path for a contract.

    Args:
        contract_id (int): The contract ID to download.
        current_user (dict): The authenticated user.

    Returns:
        dict: Path to the contract PDF.

    Raises:
        HTTPException: If the contract is not found.
    """
    contract_pdf = await get_contract_pdf(contract_id)
    if not contract_pdf:
        raise HTTPException(status_code=404, detail="Contract PDF not found")

    return contract_pdf
