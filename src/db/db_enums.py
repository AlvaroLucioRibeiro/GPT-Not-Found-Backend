from enum import Enum


class OrderStatus(str, Enum):
    """
    Enum representing possible order statuses.
    """

    PENDING = "pending"
    PAID = "paid"
    CANCELED = "canceled"


class UserType(str, Enum):
    """
    Enum representing user roles.
    """

    CUSTOMER = "customer"
    ADMIN = "admin"


class EventType(str, Enum):
    """
    Enum representing different event types.
    """

    WEDDING = "wedding"
    CORPORATE = "corporate"
    DEBUTANTE = "debutante"
    OTHER = "other"


class ProductType(str, Enum):
    """
    Enum representing different product categories.
    """

    DRINK = "drink"
    STRUCTURE = "structure"
    SERVICE = "service"


class PaymentMethod(str, Enum):
    """
    Enum representing available payment methods.
    """

    CREDIT_CARD = "credit_card"
    PIX = "pix"
    BOLETO = "boleto"
    BANK_TRANSFER = "bank_transfer"


class PaymentStatus(str, Enum):
    """
    Enum representing possible payment statuses.
    """

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
