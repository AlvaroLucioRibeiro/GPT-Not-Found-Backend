import unittest
from faker import Faker
from src.db.db_base_classes import Customer

fake = Faker()

class CustomerTest(unittest.TestCase):
    """Unit test for the Customer class"""

    def generate_random_customer(self):
        """Generates a random Customer instance"""
        return Customer(
            full_name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            address=fake.address(),
            cpf_cnpj=fake.ssn(),  # O Faker pode gerar CPF, mas para CNPJ pode ser necessário um gerador específico
            password_hash=fake.sha256(),
            role=fake.random_element(elements=["customer", "admin"])
        )

    def test_create_customer(self):
        """Tests the creation of a Customer instance"""
        customer = self.generate_random_customer()
        self.assertIsInstance(customer, Customer)
        self.assertTrue(customer.full_name)
        self.assertTrue(customer.email)
        self.assertTrue(customer.phone)
        self.assertTrue(customer.address)
        self.assertTrue(customer.cpf_cnpj)
        self.assertTrue(customer.password_hash)
        self.assertIn(customer.role, ["customer", "admin"])