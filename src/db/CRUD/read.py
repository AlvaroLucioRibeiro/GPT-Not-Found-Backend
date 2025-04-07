from fastapi import HTTPException
from typing import Dict, List, Optional
from db.db_sql_connection import connect


async def get_customer_by_email(email: str) -> Optional[Dict[str, str]]:
    """
    Recovery customer data by email

    Args:
        email (str): Customer email

    return:
        Optional[Dict[str, str]]: Customer data

    exceptions:
        HTTPException: Database error
    """
    query = "SELECT id, full_name, email, phone, address, cpf_cnpj, password_hash, role FROM customers WHERE email = %s;"

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (email,))
                customer = cursor.fetchone()

        if customer:
            return {
                "id": customer[0],
                "full_name": customer[1],
                "email": customer[2],
                "phone": customer[3],
                "address": customer[4],
                "cpf_cnpj": customer[5],
                "password_hash": customer[6],
                "role": customer[7],
            }
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_event_by_id(event_id: int) -> Optional[Dict[str, str]]:
    """
    Retrieves a specific event by its ID.

    Args:
        event_id (int): The event ID.

    Returns:
        Optional[Dict[str, str]]: Event details if found, otherwise None.

    Raises:
        HTTPException: If an error occurs while fetching the event.
    """
    query = "SELECT * FROM events WHERE id = %s;"

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (event_id,))
                row = cursor.fetchone()

                if row:
                    columns = [desc[0] for desc in cursor.description]
                    event = dict(zip(columns, row))
                    return event

        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_all_events() -> List[Dict[str, str]]:
    """
    Retrieves all events from the database.

    Returns:
        List[Dict[str, str]]: A list of dictionaries representing events.

    Raises:
        HTTPException: If an error occurs while fetching events.
    """
    query = """
        SELECT id, customer_id, event_type, event_date, location, guest_count, duration_hours, budget_approved 
        FROM events;
    """

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                columns = [desc[0] for desc in cursor.description]  # Get column names
                events = [
                    dict(zip(columns, row)) for row in cursor.fetchall()
                ]  # Convert rows to dictionaries
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_order_by_id(order_id: int) -> Optional[Dict[str, str]]:
    """
    Retrieves an order by its ID.

    Args:
        order_id (int): The order identifier.

    Returns:
        Optional[Dict[str, str]]: Order details if found, otherwise None.

    Raises:
        HTTPException: If an error occurs while fetching data from the database.
    """
    query = "SELECT * FROM orders WHERE id = %(order_id)s"

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, {"order_id": order_id})
                row = cursor.fetchone()

                if row:
                    columns = [desc[0] for desc in cursor.description]
                    order = dict(zip(columns, row))
                    return order

        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_all_orders() -> List[Dict[str, str]]:
    """
    Retrieves all registered orders.

    Returns:
        List[Dict[str, str]]: List containing all orders.

    Raises:
        HTTPException: If an error occurs while fetching data from the database.
    """
    query = "SELECT * FROM orders"
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_customer_by_id(customer_id: int) -> Optional[Dict[str, str]]:
    """
    Retrieves a specific customer by their ID.

    Args:
        customer_id (int): The customer ID.

    Returns:
        Optional[Dict[str, str]]: Customer details if found, otherwise None.

    Raises:
        HTTPException: If an error occurs while fetching the customer.
    """
    query = """
        SELECT id, full_name, email, phone, address, cpf_cnpj, role, created_at, updated_at
        FROM customers 
        WHERE id = %s;
    """

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (customer_id,))
                customer = cursor.fetchone()

        if customer:
            return {
                "id": customer[0],
                "full_name": customer[1],
                "email": customer[2],
                "phone": customer[3],
                "address": customer[4],
                "cpf_cnpj": customer[5],
                "role": customer[6],
                "created_at": customer[7],
                "updated_at": customer[8],
            }
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_all_customers() -> List[Dict[str, str]]:
    """
    Retrieves all customers from the database.

    Returns:
        List[Dict[str, str]]: A list of dictionaries representing customers.

    Raises:
        HTTPException: If an error occurs while fetching customers.
    """
    query = """
        SELECT id, full_name, email, phone, address, cpf_cnpj, role, created_at, updated_at
        FROM customers;
    """

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                columns = [desc[0] for desc in cursor.description]  # Get column names
                customers = [
                    dict(zip(columns, row)) for row in cursor.fetchall()
                ]  # Convert rows to dictionaries
        return customers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_payment_by_id(payment_id: int) -> Optional[Dict[str, str]]:
    """
    Retrieves a specific payment by its ID.

    Args:
        payment_id (int): The unique identifier of the payment.

    Returns:
        Optional[Dict[str, str]]: Payment details including 'id' if found, otherwise None.

    Raises:
        HTTPException: If an error occurs while fetching the payment.
    """
    query = """
        SELECT id, order_id, amount, payment_method, status, payment_date, updated_at
        FROM payments
        WHERE id = %(payment_id)s;
    """

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, {"payment_id": payment_id})
                row = cursor.fetchone()

                if row:
                    columns = [desc[0] for desc in cursor.description]
                    payment = dict(zip(columns, row))
                    return payment

        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_product_by_id(product_id: int) -> Optional[Dict[str, str]]:
    """
    Retrieves a specific product by its ID.

    Args:
        product_id (int): The product ID.

    Returns:
        Optional[Dict[str, str]]: Product details if found, otherwise None.
    """
    query = "SELECT * FROM products WHERE id = %s;"
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (product_id,))
                row = cursor.fetchone()
                if row:
                    columns = [desc[0] for desc in cursor.description]
                    return dict(zip(columns, row))
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_all_products() -> List[Dict[str, str]]:
    """
    Retrieves all products from the database.

    Returns:
        List[Dict[str, str]]: A list of dictionaries representing products.
    """
    query = "SELECT * FROM products;"
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_invoice_by_order_id(order_id: int) -> Optional[Dict[str, str]]:
    """
    Retrieves an invoice by order ID.

    Args:
        order_id (int): The order ID.

    Returns:
        Optional[Dict[str, str]]: Invoice details if found, otherwise None.

    Raises:
        HTTPException: If an error occurs while fetching the invoice.
    """
    query = """
        SELECT id, order_id, invoice_number, issue_date, total_amount, pdf_file
        FROM invoices WHERE order_id = %(order_id)s;
    """

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, {"order_id": order_id})
                row = cursor.fetchone()

                if row:
                    columns = [desc[0] for desc in cursor.description]
                    invoice = dict(zip(columns, row))
                    return invoice

        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_invoice_pdf(invoice_id: int) -> Optional[Dict[str, str]]:
    """
    Retrieves the PDF file path for an invoice.

    Args:
        invoice_id (int): The invoice ID.

    Returns:
        Optional[Dict[str, str]]: Path to the invoice PDF if found, otherwise None.

    Raises:
        HTTPException: If an error occurs while fetching the invoice.
    """
    query = """
        SELECT pdf_file FROM invoices WHERE id = %(invoice_id)s;
    """

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, {"invoice_id": invoice_id})
                row = cursor.fetchone()

                if row:
                    return {"pdf_file": row[0]}

        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_contract_by_event_id(event_id: int) -> Optional[Dict[str, str]]:
    """
    Retrieves a contract by event ID.

    Args:
        event_id (int): The event ID.

    Returns:
        Optional[Dict[str, str]]: Contract details if found, otherwise None.

    Raises:
        HTTPException: If an error occurs while fetching the contract.
    """
    query = """
        SELECT id, event_id, created_at, updated_at, pdf_file
        FROM contracts WHERE event_id = %(event_id)s;
    """

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, {"event_id": event_id})
                row = cursor.fetchone()

                if row:
                    columns = [desc[0] for desc in cursor.description]
                    contract = dict(zip(columns, row))
                    return contract

        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_contract_pdf(contract_id: int) -> Optional[Dict[str, str]]:
    """
    Retrieves the PDF file path for a contract.

    Args:
        contract_id (int): The contract ID.

    Returns:
        Optional[Dict[str, str]]: Path to the contract PDF if found, otherwise None.

    Raises:
        HTTPException: If an error occurs while fetching the contract.
    """
    query = """
        SELECT pdf_file FROM contracts WHERE id = %(contract_id)s;
    """

    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, {"contract_id": contract_id})
                row = cursor.fetchone()

                if row:
                    return {"pdf_file": row[0]}

        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_events_by_customer_id(customer_id: int) -> List[Dict[str, str]]:
    """
    Retrieves all events associated with a specific customer.

    Args:
        customer_id (int): Customer ID.

    Returns:
        List[Dict[str, str]]: List of events.
    """
    query = """
        SELECT * FROM events WHERE customer_id = %s;
    """
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (customer_id,))
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_orders_by_customer_id(customer_id: int) -> List[Dict[str, str]]:
    """
    Retrieves all orders related to the customer's events.

    Args:
        customer_id (int): Customer ID.

    Returns:
        List[Dict[str, str]]: List of orders.
    """
    query = """
        SELECT o.* FROM orders o
        JOIN events e ON o.event_id = e.id
        WHERE e.customer_id = %s;
    """
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (customer_id,))
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_payments_by_customer_id(customer_id: int) -> List[Dict[str, str]]:
    """
    Retrieves all payments related to the customer's orders.

    Args:
        customer_id (int): Customer ID.

    Returns:
        List[Dict[str, str]]: List of payments.
    """
    query = """
        SELECT p.* FROM payments p
        JOIN orders o ON p.order_id = o.id
        JOIN events e ON o.event_id = e.id
        WHERE e.customer_id = %s;
    """
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (customer_id,))
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_invoices_by_customer_id(customer_id: int) -> List[Dict[str, str]]:
    """
    Retrieves all invoices related to the customer's orders.

    Args:
        customer_id (int): Customer ID.

    Returns:
        List[Dict[str, str]]: List of invoices.
    """
    query = """
        SELECT i.* FROM invoices i
        JOIN orders o ON i.order_id = o.id
        JOIN events e ON o.event_id = e.id
        WHERE e.customer_id = %s;
    """
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (customer_id,))
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_contracts_by_customer_id(customer_id: int) -> List[Dict[str, str]]:
    """
    Retrieves all contracts related to a customer's events.

    Args:
        customer_id (int): Customer ID.

    Returns:
        List[Dict[str, str]]: List of contracts.
    """
    query = """
        SELECT c.* FROM contracts c
        JOIN events e ON c.event_id = e.id
        WHERE e.customer_id = %s;
    """
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (customer_id,))
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
