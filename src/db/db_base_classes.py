from pydantic import BaseModel

class Customer(BaseModel):
    """
    A class used to represent a Customer.

    Attributes
    ----------
    full_name : str
        The full name of the customer.
    email : str
        The email address of the customer.
    phone : str
        The phone number of the customer.
    address : str
        The physical address of the customer.
    cpf_cnpj : str
        The CPF or CNPJ (Brazilian individual or company taxpayer registry identification) of the customer.
    password_hash : str
        The hashed password of the customer.
    role : str
        The role of the customer in the system.
    """
    full_name: str
    email: str
    phone: str
    address: str
    cpf_cnpj: str
    password_hash: str
    role: str