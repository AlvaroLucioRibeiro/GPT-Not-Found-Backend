from typing import Dict, Optional
from fastapi import HTTPException
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
