"""
Módulo de pruebas unitarias para la clase Hotel.
Incluye casos positivos y negativos para cumplir con la cobertura del 85%.
"""
import unittest
import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


from hotel import Hotel

class TestHotel(unittest.TestCase):
    """Clase de pruebas para validar la funcionalidad de Hotel."""

    def setUp(self):
        """Configuración antes de cada prueba: define un archivo temporal."""
        self.test_file = "data/test_hotels.json"
        # Asegurar que la carpeta exista
        os.makedirs(os.path.dirname(self.test_file), exist_ok=True)
        # Limpiar archivo si existe
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        """Limpieza después de cada prueba."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    # --- CASOS POSITIVOS ---

    def test_create_hotel_success(self):
        """Verifica la creación y guardado exitoso de un hotel."""
        hotel = Hotel.create_hotel(1, "Playa Azul", "Cancún", 10, self.test_file)
        self.assertEqual(hotel.name, "Playa Azul")
        self.assertTrue(os.path.exists(self.test_file))

    def test_display_hotel_info(self):
        """Verifica que se pueda recuperar la información de un hotel."""
        Hotel.create_hotel(1, "Playa Azul", "Cancún", 10, self.test_file)
        hotel = Hotel.display_hotel(1, self.test_file)
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel.location, "Cancún")

    # --- CASOS NEGATIVOS (Requerimiento 3 y 5) ---

    def test_load_corrupt_json(self):
        """Caso Negativo 1: El archivo tiene un formato JSON inválido."""
        with open(self.test_file, 'w', encoding='utf-8') as file:
            file.write("esto_no_es_un_json")
        # Debe manejar el error sin detener la ejecución (Req 5)
        hotels = Hotel.load_hotels(self.test_file)
        self.assertEqual(hotels, [])

    def test_delete_non_existent_id(self):
        """Caso Negativo 2: Intentar eliminar un ID que no existe."""
        Hotel.create_hotel(1, "Hotel A", "Sinaloa", 5, self.test_file)
        # No debe lanzar excepción ni borrar el hotel existente
        Hotel.delete_hotel(99, self.test_file)
        hotels = Hotel.load_hotels(self.test_file)
        self.assertEqual(len(hotels), 1)

    def test_reserve_no_rooms_available(self):
        """Caso Negativo 3: Intentar reservar con 0 habitaciones disponibles."""
        hotel = Hotel(1, "Hotel Lleno", "CDMX", 0)
        result = hotel.reserve_room(self.test_file)
        self.assertFalse(result)

    def test_load_missing_data_keys(self):
        """Caso Negativo 4: JSON válido pero con llaves faltantes."""
        bad_data = [{"hotel_id": 1, "name": "Incompleto"}]  # Falta 'rooms'
        with open(self.test_file, 'w', encoding='utf-8') as file:
            json.dump(bad_data, file)
        # El programa debe manejar el error y retornar lista vacía
        hotels = Hotel.load_hotels(self.test_file)
        self.assertEqual(hotels, [])

    def test_modify_non_existent_hotel(self):
        """Caso Negativo 5: Intentar modificar un hotel que no existe."""
        Hotel.create_hotel(1, "Original", "Mérida", 10, self.test_file)
        Hotel.modify_hotel(50, self.test_file, name="No Existe")
        # El original debe permanecer sin cambios
        hotels = Hotel.load_hotels(self.test_file)
        self.assertEqual(hotels[0].name, "Original")


if __name__ == '__main__':
    unittest.main()
