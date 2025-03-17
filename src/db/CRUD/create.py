from typing import Dict
from fastapi import HTTPException
from db.db_sql_connection import connect


async def create_customer(customer_data: Dict[str, str]) -> Dict[str, str]:
    """
    Insere um novo cliente na tabela customers.

    Args:
        customer_data (Dict[str, str]): Dicionário contendo os dados do cliente.

    Returns:
        Dict[str, str]: Mensagem de sucesso ou erro.

    Raises:
        HTTPException: Se ocorrer um erro ao inserir os dados no banco.
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
        return {"message": "Cliente cadastrado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def create_order(order_data: Dict[str, str]) -> Dict[str, str]:
    """
    Inserts a new order into the orders table.

    Args:
        order_data (Dict[str, str]): Dictionary containing the order details.

    Returns:
        Dict[str, str]: Success or error message.

    Raises:
        HTTPException: If an error occurs while inserting data into the database.
    """
    query = """
        INSERT INTO orders (event_id, order_date, total_amount, status)
        VALUES (%(event_id)s, %(order_date)s, %(total_amount)s, %(status)s);
    """
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, order_data)
            conn.commit()
        return {"message": "Order successfully created!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
