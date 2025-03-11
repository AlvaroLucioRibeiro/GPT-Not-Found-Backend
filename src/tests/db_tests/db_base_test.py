import pytest
from pydantic import ValidationError
from src.db.db_base_classes import Customer


def test_valid_customer():
    """
    Tests the creation of a valid customer instance.
    """
    customer_data = {
        "full_name": "Alvaro Ribeiro",
        "email": "alvaro@inatel.br",
        "phone": "35 99988-7766",
        "address": "Rua Joao de Camargo, 510, Santa Rita do Sapucai",
        "cpf_cnpj": "123.456.789-09",
        "password_hash": "hashed_password",
        "role": "customer",
    }
    customer = Customer(**customer_data)
    assert customer.full_name == "Alvaro Ribeiro"
    assert customer.email == "alvaro@inatel.br"
    assert customer.phone == "35 99988-7766"
    assert customer.address == "Rua Joao de Camargo, 510, Santa Rita do Sapucai"
    assert customer.cpf_cnpj == "123.456.789-09"
    assert customer.password_hash == "hashed_password"
    assert customer.role == "customer"


def test_invalid_customer_missing_fields():
    """
    Tests if an error is raised when attempting to create a customer without required fields.
    """
    with pytest.raises(ValidationError):
        Customer(
            full_name="Alvaro Ribeiro", email="alvaro@inatel.br"
        )  # Missing required fields


def test_invalid_email_format():
    """
    Tests if an error is raised for an invalid email format.
    """
    with pytest.raises(ValidationError):
        Customer(
            full_name="Alvaro Ribeiro",
            email="alvaro@invalid",
            phone="35 99988-7766",
            address="Rua Joao de Camargo, 510, Santa Rita do Sapucai",
            cpf_cnpj="123.456.789-09",
            password_hash="hashed_password",
            role="customer",
        )


def test_invalid_cpf_cnpj():
    """
    Tests if an error is raised for an invalid CPF/CNPJ format.
    """
    with pytest.raises(ValidationError):
        Customer(
            full_name="Alvaro Ribeiro",
            email="alvaro@inatel.br",
            phone="35 99988-7766",
            address="Rua Joao de Camargo, 510, Santa Rita do Sapucai",
            cpf_cnpj="invalid_cpf",
            password_hash="hashed_password",
            role="customer",
        )
