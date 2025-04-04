from typing import List, Dict
from utils.utils_token_auth import get_current_user
from fastapi import APIRouter, HTTPException, Path, Depends
from db.CRUD.read import (
    get_events_by_customer_id,
    get_orders_by_customer_id,
    get_payments_by_customer_id,
    get_invoices_by_customer_id,
    get_contracts_by_customer_id,
)

customers_router_data = APIRouter(prefix="/customers", tags=["Customers Data"])


@customers_router_data.get("/{customer_id}/events", response_model=List[Dict])
async def fetch_events_by_customer(
    customer_id: int = Path(..., gt=0), current_user: dict = Depends(get_current_user)
):
    """
    Returns all events associated with the given customer ID.
    """
    events = await get_events_by_customer_id(customer_id)
    if not events:
        raise HTTPException(
            status_code=404, detail="No events found for this customer."
        )
    return events


@customers_router_data.get("/{customer_id}/orders", response_model=List[Dict])
async def fetch_orders_by_customer(
    customer_id: int = Path(..., gt=0), current_user: dict = Depends(get_current_user)
):
    """
    Returns all orders associated with the given customer ID.
    """
    orders = await get_orders_by_customer_id(customer_id)
    if not orders:
        raise HTTPException(
            status_code=404, detail="No orders found for this customer."
        )
    return orders


@customers_router_data.get("/{customer_id}/payments", response_model=List[Dict])
async def fetch_payments_by_customer(
    customer_id: int = Path(..., gt=0), current_user: dict = Depends(get_current_user)
):
    """
    Returns all payments associated with the given customer ID.
    """
    payments = await get_payments_by_customer_id(customer_id)
    if not payments:
        raise HTTPException(
            status_code=404, detail="No payments found for this customer."
        )
    return payments


@customers_router_data.get("/{customer_id}/invoices", response_model=List[Dict])
async def fetch_invoices_by_customer(
    customer_id: int = Path(..., gt=0), current_user: dict = Depends(get_current_user)
):
    """
    Returns all invoices associated with the given customer ID.
    """
    invoices = await get_invoices_by_customer_id(customer_id)
    if not invoices:
        raise HTTPException(
            status_code=404, detail="No invoices found for this customer."
        )
    return invoices


@customers_router_data.get("/{customer_id}/contracts", response_model=List[Dict])
async def fetch_contracts_by_customer(
    customer_id: int = Path(..., gt=0), current_user: dict = Depends(get_current_user)
):
    """
    Returns all contracts associated with the given customer ID.
    """
    contracts = await get_contracts_by_customer_id(customer_id)
    if not contracts:
        raise HTTPException(
            status_code=404, detail="No contracts found for this customer."
        )
    return contracts
