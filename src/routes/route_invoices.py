from fastapi import APIRouter, HTTPException, Depends, Query
from db.CRUD.read import get_invoice_by_order_id, get_invoice_pdf
from utils.utils_token_auth import get_current_user

invoices_router = APIRouter(prefix="/invoices", tags=["Invoices"])


@invoices_router.get("/")
async def get_invoice(
    order_id: int = Query(..., description="The order identifier"),
    current_user: dict = Depends(get_current_user),
):
    """
    Retrieves invoices related to a specific order.

    Args:
        order_id (int): The order ID to fetch invoices for.
        current_user (dict): The authenticated user.

    Returns:
        dict: Invoice details.

    Raises:
        HTTPException: If the invoice is not found.
    """
    invoice = await get_invoice_by_order_id(order_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    return invoice


@invoices_router.get("/download/")
async def download_invoice(
    invoice_id: int,
    current_user: dict = Depends(get_current_user),
):
    """
    Retrieves the PDF file path for an invoice.

    Args:
        invoice_id (int): The invoice ID to download.
        current_user (dict): The authenticated user.

    Returns:
        dict: Path to the invoice PDF.

    Raises:
        HTTPException: If the invoice is not found.
    """
    invoice_pdf = await get_invoice_pdf(invoice_id)
    if not invoice_pdf:
        raise HTTPException(status_code=404, detail="Invoice PDF not found")

    return invoice_pdf
