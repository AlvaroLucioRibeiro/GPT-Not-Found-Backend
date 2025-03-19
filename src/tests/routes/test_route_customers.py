import pytest
from faker import Faker
from src.tests.db_tests.db_classes import CustomerTest  # Importe a classe de testes do diretório correto
from src.db.CRUD.read import get_customer_by_id, get_all_customers
from src.db.CRUD.create import create_customer
from src.db.CRUD.update import update_customer
from src.db.CRUD.delete import delete_customer

fake = Faker()

class CustomerCRUDTest(CustomerTest):
    """Unit tests for Customer CRUD operations"""

    @pytest.mark.asyncio
    async def test_get_customer_by_id(self):
        """Test retrieving a customer by ID"""
        customer = await get_customer_by_id(2)
        self.assertIsNotNone(customer)
        self.assertEqual(customer["id"], 2)
        self.assertEqual(customer["full_name"], "Teste")

    @pytest.mark.asyncio
    async def test_get_all_customers(self):
        """Test retrieving all customers"""
        customers = await get_all_customers()
        self.assertIsInstance(customers, list)
        self.assertGreater(len(customers), 0)
        self.assertEqual(customers[0]["email"], "teste@gmail.com")

    @pytest.mark.asyncio
    async def test_create_customer(self):
        """Test creating a new customer"""
        new_customer_data = {
            "full_name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "address": fake.address(),
            "cpf_cnpj": "123.456.789-09",  # CPF fictício
            "password_hash": fake.sha256(),
            "role": fake.random_element(elements=["customer", "admin"]),
        }

        customer = await create_customer(new_customer_data)
        self.assertIsNotNone(customer)
        self.assertIn("id", customer)
        self.assertEqual(customer["full_name"], new_customer_data["full_name"])

    @pytest.mark.asyncio
    async def test_update_customer(self):
        """Test updating a customer"""
        update_data = {
            "full_name": "Alvaro Atualizado",
            "email": "alvaro@inatel.br",
        }

        updated_customer = await update_customer(1, update_data)
        self.assertEqual(updated_customer["full_name"], "Alvaro Atualizado")
        self.assertIn("phone", updated_customer)  # Verifica se 'phone' ainda está presente

    @pytest.mark.asyncio
    async def test_delete_customer(self):
        """Test deleting a customer"""
        result = await delete_customer(1)
        self.assertTrue(result)
