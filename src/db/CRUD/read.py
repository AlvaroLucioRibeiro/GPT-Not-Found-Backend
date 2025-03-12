from typing import Dict, Optional
from fastapi import HTTPException
from db.db_sql_connection import connect


async def get_customer_by_email(email: str) -> Optional[Dict[str, str]]:
    """
    Recupera um cliente pelo email da tabela customers.

    Args:
        email (str): Email do cliente.

    Returns:
        Optional[Dict[str, str]]: Dicionário contendo os dados do cliente se encontrado, ou None se não existir.

    Raises:
        HTTPException: Se ocorrer um erro na consulta ao banco de dados.
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
        return None  # Retorna None caso o email não exista
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))