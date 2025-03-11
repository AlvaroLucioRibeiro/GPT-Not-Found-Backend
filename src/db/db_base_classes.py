import re
from pydantic import BaseModel, EmailStr, field_validator

class Customer(BaseModel):
    """
    Represents a Customer in the system.

    Attributes:
        full_name (str): The full name of the customer.
        email (EmailStr): The email address of the customer.
        phone (str): The phone number of the customer.
        address (str): The physical address of the customer.
        cpf_cnpj (str): The CPF or CNPJ (Brazilian taxpayer registry identification) of the customer.
        password_hash (str): The hashed password of the customer.
        role (str): The role of the customer in the system.
    """

    full_name: str
    email: EmailStr 
    phone: str
    address: str
    cpf_cnpj: str
    password_hash: str
    role: str

    @field_validator("cpf_cnpj")
    @classmethod
    def validate_cpf_cnpj(cls, value: str) -> str:
        """
        Validates if the CPF/CNPJ is in the correct format.

        CPF format: 000.000.000-00
        CNPJ format: 00.000.000/0000-00

        Args:
            value (str): The CPF or CNPJ value to validate.

        Returns:
            str: The validated CPF or CNPJ.

        Raises:
            ValueError: If the CPF/CNPJ is not in the correct format.
        """
        cpf_cnpj_pattern = re.compile(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$")
        if not cpf_cnpj_pattern.match(value):
            raise ValueError("Invalid CPF/CNPJ. Use the correct format: 000.000.000-00 or 00.000.000/0000-00")
        return value
