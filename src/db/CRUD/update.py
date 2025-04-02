from typing import Dict
from fastapi import HTTPException
from db.db_sql_connection import connect


async def update_order(order_id: int, order_data: Dict[str, str]) -> Dict[str, str]:
    """
    Updates an existing order in the orders table.

    Args:
        order_id (int): The order identifier.
        order_data (Dict[str, str]): Updated order details.

    Returns:
        Dict[str, str]: Success or error message.

    Raises:
        HTTPException: If an error occurs while updating data in the database.
    """
    query = """
        UPDATE orders
        SET event_id = %(event_id)s, order_date = %(order_date)s, total_amount = %(total_amount)s, status = %(status)s
        WHERE id = %(order_id)s;
    """
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, {"order_id": order_id, **order_data})
            conn.commit()
        return {"message": "Order successfully updated!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_event(event_id: int, event_data: Dict[str, str]) -> Dict[str, str]:
    """
    Updates an existing event.

    Args:
        event_id (int): The event ID.
        event_data (Dict[str, str]): Updated event data.

    Returns:
        Dict[str, str]: Success message.

    Raises:
        HTTPException: If the update fails or the event is not found.
    """
    query = """
        UPDATE events
        SET event_type = %(event_type)s,
            event_date = %(event_date)s,
            location = %(location)s,
            guest_count = %(guest_count)s,
            duration_hours = %(duration_hours)s,
            budget_approved = %(budget_approved)s,
            updated_at = NOW()
        WHERE id = %(event_id)s
        RETURNING *;
    """

    # Add the event_id to the event_data dictionary
    event_data["event_id"] = event_id

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, event_data)
                updated_event = cursor.fetchone()

            if not updated_event:
                raise HTTPException(
                    status_code=404, detail="Event not found or update failed"
                )

            conn.commit()
        return {"message": "Event successfully updated!", "event": updated_event}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_customer(
    customer_id: int, customer_data: Dict[str, str]
) -> Dict[str, str]:
    """
    Updates an existing customer in the 'customers' table.

    Args:
        customer_id (int): The customer identifier.
        customer_data (Dict[str, str]): Updated customer details.

    Returns:
        Dict[str, str]: Success message with updated customer details.

    Raises:
        HTTPException: If an error occurs while updating data in the database.
    """
    query = """
        UPDATE customers
        SET full_name = %(full_name)s,
            email = %(email)s,
            phone = %(phone)s,
            address = %(address)s,
            cpf_cnpj = %(cpf_cnpj)s,
            role = %(role)s,
            updated_at = NOW()
        WHERE id = %(customer_id)s
        RETURNING id, full_name, email, phone, address, cpf_cnpj, role, created_at, updated_at;
    """

    customer_data["customer_id"] = customer_id  # Add customer_id to the data dictionary

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, customer_data)
                updated_customer = cursor.fetchone()

            if not updated_customer:
                raise HTTPException(
                    status_code=404, detail="Customer not found or update failed"
                )

            conn.commit()
        return {"message": "Customer successfully updated!", "customer": updated_customer}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_payment(
    payment_id: int, payment_data: Dict[str, str]
) -> Dict[str, str]:
    """
    Updates an existing payment record in the 'payments' table.

    Args:
        payment_id (int): The unique identifier of the payment.
        payment_data (Dict[str, str]): Dictionary containing the updated payment details.

    Returns:
        Dict[str, str]: Success message with updated payment details.

    Raises:
        HTTPException: If the payment is not found or if an error occurs during the update.
    """
    query = """
        UPDATE payments
        SET amount = %(amount)s,
            payment_method = %(payment_method)s,
            status = %(status)s,
            payment_date = %(payment_date)s,
            updated_at = NOW()
        WHERE id = %(payment_id)s
        RETURNING *;
    """

    # Add the payment_id to the payment_data dictionary
    payment_data["payment_id"] = payment_id

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, payment_data)
                updated_payment = cursor.fetchone()

            if not updated_payment:
                raise HTTPException(
                    status_code=404, detail="Payment not found or update failed"
                )

            conn.commit()
        return {"message": "Payment successfully updated!", "payment": updated_payment}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_product(
    product_id: int, product_data: Dict[str, str]
) -> Dict[str, str]:
    """
    Updates an existing product.

    Args:
        product_id (int): The product ID.
        product_data (Dict[str, str]): The updated product data.
    
    Returns:
        Dict[str, str]: The updated product details.
    """
    query = """
        UPDATE products
        SET name = %(name)s,
            description = %(description)s,
            base_price = %(base_price)s,
            category = %(category)s,
            active = %(active)s,
            updated_at = NOW()
        WHERE id = %(product_id)s
        RETURNING *;
    """
    product_data["product_id"] = product_id
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, product_data)
                updated_product = cursor.fetchone()
                if not updated_product:
                    raise HTTPException(status_code=404, detail="Product not found")
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, updated_product))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
