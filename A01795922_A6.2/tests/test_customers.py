"""Módulo de pruebas unitarias para la clase Customer."""
import unittest
import os
import sys
import json

# Añadir la raíz al path para que reconozca la carpeta src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.customers import Customer

class TestCustomer(unittest.TestCase):
    """Pruebas para validar la funcionalidad de la clase Customer."""

    def setUp(self):
        """Configuración de archivos temporales."""
        self.test_file = "data/test_customers.json"
        os.makedirs(os.path.dirname(self.test_file), exist_ok=True)
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        """Limpieza de archivos."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_create_customer_success(self):
        """Este test ahora coincidirá con la clase."""
        data = {
            "customer_id": 101, 
            "name": "Juan Perez", 
            "email": "juan@mail.com"
        }
        cust = Customer.create_customer(data, self.test_file)
        self.assertEqual(cust.name, "Juan Perez")

    def test_display_customer_success(self):
        """Caso Positivo: Recuperar información de un cliente."""
        data = {"customer_id": 102, "name": "Ana", "email": "ana@mail.com"}
        Customer.create_customer(data, self.test_file)
        result = Customer.display_customer(102, self.test_file)
        self.assertIsNotNone(result)

    def test_modify_customer_success(self):
        """Caso Positivo: Modificar datos de un cliente."""
        data = {"customer_id": 103, "name": "Original", "email": "o@mail.com"}
        Customer.create_customer(data, self.test_file)
        Customer.modify_customer(103, self.test_file, name="Modificado")
        customers = Customer.load_customers(self.test_file)
        self.assertEqual(customers[0].name, "Modificado")

    def test_load_corrupt_json(self):
        """Caso Negativo: Manejo de archivo corrupto (Req 5)."""
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write("invalido")
        customers = Customer.load_customers(self.test_file)
        self.assertEqual(customers, [])

    def test_delete_customer_success(self):
        """Caso Positivo: Eliminar un cliente."""
        data = {"customer_id": 104, "name": "A borrar", "email": "b@mail.com"}
        Customer.create_customer(data, self.test_file)
        Customer.delete_customer(104, self.test_file)
        self.assertEqual(len(Customer.load_customers(self.test_file)), 0)
