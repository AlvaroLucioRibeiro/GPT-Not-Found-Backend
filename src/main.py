from db.sql_connection import connect
from typing import Dict
from fastapi import HTTPException


def create_customer(customer_data: Dict[str, str]) -> Dict[str, str]:
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


# Exemplo de uso
if __name__ == "__main__":
    new_customer = {
        "full_name": "João Silva",
        "email": "joao.silva@example.com",
        "phone": "11999999999",
        "address": "Rua das Flores, 123, São Paulo - SP",
        "cpf_cnpj": "123.456.789-00",
        "password_hash": "senha_criptografada",
        "role": "customer",
    }
    
    result = create_customer(new_customer)
    print(result)