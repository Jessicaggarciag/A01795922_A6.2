"""Módulo para la gestión de clientes y persistencia en JSON."""
import json
import os


class Customer:
    """Clase para representar y gestionar un Cliente."""

    def __init__(self, customer_id, name, email):
        """Inicializa los atributos del cliente."""
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def to_dict(self):
        """Convierte la instancia a diccionario."""
        return self.__dict__

    @classmethod
    def create_customer(cls, data, filename):
        """Crea un cliente usando un diccionario"""
        customers = cls.load_customers(filename)
        # Extraemos las llaves del diccionario que mandamos en el test
        new_cust = cls(data['customer_id'], data['name'], data['email'])
        customers.append(new_cust)
        cls.save_to_file(filename, customers)
        return new_cust

    @staticmethod
    def delete_customer(cust_id, filename):
        """Elimina un cliente por su ID."""
        customers = Customer.load_customers(filename)
        updated = [c for c in customers if c.customer_id != cust_id]
        Customer.save_to_file(filename, updated)

    @staticmethod
    def display_customer(cust_id, filename):
        """Muestra la información de un cliente."""
        customers = Customer.load_customers(filename)
        for cust in customers:
            if cust.customer_id == cust_id:
                print(f"ID: {cust.customer_id} | Nombre: {cust.name} "
                      f"| Email: {cust.email}")
                return cust
        print("Cliente no encontrado.")
        return None

    @staticmethod
    def modify_customer(cust_id, filename, **kwargs):
        """Modifica la información de un cliente."""
        customers = Customer.load_customers(filename)
        for cust in customers:
            if cust.customer_id == cust_id:
                cust.name = kwargs.get('name', cust.name)
                cust.email = kwargs.get('email', cust.email)
                break
        Customer.save_to_file(filename, customers)

    @staticmethod
    def load_customers(filename):
        """Carga clientes manejando datos inválidos."""
        if not os.path.exists(filename):
            return []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [Customer(**c) for c in data]
        except (json.JSONDecodeError, TypeError, KeyError) as error:
            print(f"Error de datos en clientes: {error}")
            return []

    @staticmethod
    def save_to_file(filename, customers):
        """Guarda la lista en el archivo persistente."""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump([c.to_dict() for c in customers], file, indent=4)
        except IOError as error:
            print(f"Error al guardar clientes: {error}")
