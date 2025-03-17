import re
from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator, Field
from db.db_enums import OrderStatus


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
        cpf_cnpj_pattern = re.compile(
            r"^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$"
        )
        if not cpf_cnpj_pattern.match(value):
            raise ValueError(
                "Invalid CPF/CNPJ. Use the correct format: 000.000.000-00 or 00.000.000/0000-00"
            )
        return value


class Order(BaseModel):
    """
    Represents an Order in the system.

    Attributes:
        event_id (int): The ID of the event associated with the order.
        order_date (datetime): The date and time when the order was created.
        total_amount (float): The total amount of the order.
        status (OrderStatus): The status of the order ('pending', 'paid', 'canceled').
    """

    event_id: int
    order_date: datetime = Field(default_factory=datetime.utcnow)
    total_amount: float
    status: OrderStatus = OrderStatus.PENDING

    @field_validator("total_amount")
    @classmethod
    def validate_total_amount(cls, value: float) -> float:
        """
        Validates that the total amount is greater than zero.

        Args:
            value (float): The total amount.

        Returns:
            float: The validated total amount.

        Raises:
            ValueError: If the total amount is not positive.
        """
        if value <= 0:
            raise ValueError("Total amount must be greater than zero.")
        return value

    @field_validator("order_date")
    @classmethod
    def validate_order_date(cls, value: datetime) -> datetime:
        """
        Ensures that the order date is not in the future.

        Args:
            value (datetime): The order date.

        Returns:
            datetime: The validated order date.

        Raises:
            ValueError: If the order date is in the future.
        """
        if value > datetime.utcnow():
            raise ValueError("Order date cannot be in the future.")
        return value
