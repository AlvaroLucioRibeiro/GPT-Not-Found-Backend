import pytest
from src.db.CRUD.read import get_invoice_by_order_id, get_invoice_pdf


@pytest.mark.asyncio
async def test_get_invoice_by_order_id_success():
    """
    Test retrieving an invoice using the order_id."""
    order_id = 3001  # already exists in the database
    invoice = await get_invoice_by_order_id(order_id)
    assert invoice is not None
    assert invoice["order_id"] == order_id
    assert invoice["invoice_number"] == "NF-001"


@pytest.mark.asyncio
async def test_get_invoice_by_order_id_not_found():
    """
    Test retrieving an invoice using a non-existent order_id."""
    order_id = 999999  # don't exist in the database
    invoice = await get_invoice_by_order_id(order_id)
    assert invoice is None


@pytest.mark.asyncio
async def test_get_invoice_pdf_success():
    """
    Test retrieving the PDF file path for an invoice using its invoice_id."""
    invoice_id = 7001
    pdf_data = await get_invoice_pdf(invoice_id)
    assert pdf_data is not None
    assert pdf_data["pdf_file"] == "nf_001.pdf"


@pytest.mark.asyncio
async def test_get_invoice_pdf_not_found():
    """
    Test retrieving the PDF file path for a non-existent invoice_id."""
    invoice_id = 999999
    pdf_data = await get_invoice_pdf(invoice_id)
    assert pdf_data is None
