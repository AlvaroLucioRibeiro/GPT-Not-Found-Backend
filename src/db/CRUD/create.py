from typing import Dict
from fastapi import HTTPException
from db.db_sql_connection import connect


async def create_customer(customer_data: Dict[str, str]) -> Dict[str, str]:
    """
    Insert a new customer into the customers table.

    Args:
        customer_data (Dict[str, str]): Dictionary with customer data.

    Returns:
        Dict[str, str]: Message confirming the customer was inserted.

    Raises:
        HTTPException: If an error occurs while trying to insert the customer.
    """
    query = """
        INSERT INTO customers (full_name, email, phone, address, cpf_cnpj, password_hash, role)
        VALUES (%(full_name)s, %(email)s, %(phone)s, %(address)s, %(cpf_cnpj)s, %(password_hash)s, %(role)s);
    """

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, customer_data)
            conn.commit()
        return {"message": "Customer inserted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def create_event(event_data: Dict[str, str]) -> Dict[str, str]:
    """
    Inserts a new event into the 'events' table.

    Args:
        event_data (Dict[str, str]): Dictionary containing the event details.

    Returns:
        Dict[str, str]: Success message.

    Raises:
        HTTPException: If an error occurs while inserting the event into the database.
    """
    query = """
        INSERT INTO events (customer_id, event_type, event_date, location, guest_count, duration_hours, budget_approved)
        VALUES (%(customer_id)s, %(event_type)s, %(event_date)s, %(location)s, %(guest_count)s, %(duration_hours)s, %(budget_approved)s)
        RETURNING id;
    """

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, event_data)
                new_event_id = cursor.fetchone()[0]
            conn.commit()
        return {"message": "Event successfully created!", "event_id": new_event_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def create_order(order_data: Dict[str, str]) -> Dict[str, str]:
    """
    Inserts a new order into the orders table.

    Args:
        order_data (Dict[str, str]): Dictionary containing the order details.

    Returns:
        Dict[str, str]: Success message with order ID.

    Raises:
        HTTPException: If an error occurs while inserting data into the database.
    """
    query = """
        INSERT INTO orders (event_id, order_date, total_amount, status)
        VALUES (%(event_id)s, %(order_date)s, %(total_amount)s, %(status)s)
        RETURNING id;
    """
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, order_data)
                order_id = cursor.fetchone()[0]
            conn.commit()
        return {"message": "Order successfully created!", "order_id": order_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def create_payment(payment_data: Dict[str, str]) -> Dict[str, str]:
    """
    Inserts a new payment into the 'payments' table.

    Args:
        payment_data (Dict[str, str]): Dictionary containing the payment details.

    Returns:
        Dict[str, str]: Success message including the inserted payment ID.

    Raises:
        HTTPException: If an error occurs while inserting the payment into the database.
    """
    query = """
        INSERT INTO payments (order_id, amount, payment_method, status, payment_date)
        VALUES (%(order_id)s, %(amount)s, %(payment_method)s, %(status)s, %(payment_date)s)
        RETURNING id;
    """
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, payment_data)
                new_payment_id = cursor.fetchone()[0]  # Captura o ID inserido
            conn.commit()
        return {
            "message": "Payment created successfully!",
            "payment_id": new_payment_id,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def create_product(product_data: Dict[str, str]) -> Dict[str, str]:
    """
    Inserts a new product into the 'products' table.

    Args:
        product_data (Dict[str, str]): Dictionary containing the product details.

    Returns:
        Dict[str, str]: Success message and created product ID.
    """
    query = """
        INSERT INTO products (name, description, base_price, category, active)
        VALUES (%(name)s, %(description)s, %(base_price)s, %(category)s, %(active)s)
        RETURNING id;
    """
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, product_data)
                product_id = cursor.fetchone()[0]
            conn.commit()
        return {"message": "Product created successfully!", "product_id": product_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def create_contract(contract_data: Dict[str, str]) -> Dict[str, str]:
    """
    Inserts a new contract into the 'contracts' table.

    Args:
        contract_data (Dict[str, str]): Dictionary containing the contract details.

    Returns:
        Dict[str, str]: Success message with contract ID.

    Raises:
        HTTPException: If an error occurs while inserting the contract.
    """
    query = """
        INSERT INTO contracts (event_id, created_at, updated_at, pdf_file)
        VALUES (%(event_id)s, NOW(), NOW(), %(pdf_file)s)
        RETURNING id;
    """

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, contract_data)
                contract_id = cursor.fetchone()[0]
            conn.commit()

        return {"message": "Contract created successfully!", "contract_id": contract_id}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error creating contract: {str(e)}"
        )
