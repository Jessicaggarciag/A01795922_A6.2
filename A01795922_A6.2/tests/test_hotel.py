"""
Módulo de pruebas unitarias para la clase Hotel.
"""
import unittest
import os
import sys
import json

# Añadir el directorio raíz al path para reconocer 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hotel import Hotel  # Importación corregida para la estructura de paquetes


class TestHotel(unittest.TestCase):
    """Clase de pruebas para validar la funcionalidad de Hotel."""

    def setUp(self):
        """Configuración antes de cada prueba: define un archivo temporal."""
        self.test_file = "data/test_hotels.json"
        os.makedirs(os.path.dirname(self.test_file), exist_ok=True)
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        """Limpieza después de cada prueba."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    # --- CASOS POSITIVOS ---

    def test_create_hotel_success(self):
        """Verifica la creación exitosa usando un diccionario"""
        hotel_data = {
            "hotel_id": 1,
            "name": "Playa Azul",
            "location": "Cancun",
            "rooms": 10
        }
        hotel = Hotel.create_hotel(hotel_data, self.test_file)
        self.assertEqual(hotel.name, "Playa Azul")

    def test_display_hotel_info(self):
        """Verifica la recuperación de información"""
        data = {"hotel_id": 1, "name": "Playa Azul", "location": "Cancun", "rooms": 10}
        Hotel.create_hotel(data, self.test_file)
        hotel = Hotel.display_hotel(1, self.test_file)
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel.location, "Cancun")

    def test_modify_hotel_success(self):
        """Verifica modificación exitosa"""
        data = {"hotel_id": 1, "name": "Original", "location": "Mérida", "rooms": 10}
        Hotel.create_hotel(data, self.test_file)
        Hotel.modify_hotel(1, self.test_file, name="Modificado", rooms=20)
        hotels = Hotel.load_hotels(self.test_file)
        self.assertEqual(hotels[0].name, "Modificado")
        self.assertEqual(hotels[0].rooms, 20)

    # --- CASOS NEGATIVOS ---

    def test_load_corrupt_json(self):
        """Caso Negativo 1: JSON inválido"""
        with open(self.test_file, 'w', encoding='utf-8') as file:
            file.write("esto_no_es_un_json")
        hotels = Hotel.load_hotels(self.test_file)
        self.assertEqual(hotels, [])

    def test_delete_non_existent_id(self):
        """Caso Negativo 2: Borrar ID inexistente."""
        data = {"hotel_id": 1, "name": "Hotel A", "location": "Sinaloa", "rooms": 5}
        Hotel.create_hotel(data, self.test_file)
        Hotel.delete_hotel(99, self.test_file)
        hotels = Hotel.load_hotels(self.test_file)
        self.assertEqual(len(hotels), 1)

    def test_reserve_no_rooms_available(self):
        """Caso Negativo 3: Sin disponibilidad"""
        hotel = Hotel(1, "Hotel Lleno", "CDMX", 0)
        result = hotel.reserve_room(self.test_file)
        self.assertFalse(result)

    def test_load_missing_data_keys(self):
        """Caso Negativo 4: Llaves faltantes"""
        bad_data = [{"hotel_id": 1, "name": "Incompleto"}]
        with open(self.test_file, 'w', encoding='utf-8') as file:
            json.dump(bad_data, file)
        hotels = Hotel.load_hotels(self.test_file)
        self.assertEqual(hotels, [])

    def test_modify_non_existent_hotel(self):
        """Caso Negativo 5: Modificar hotel inexistente."""
        data = {"hotel_id": 1, "name": "Original", "location": "Mérida", "rooms": 10}
        Hotel.create_hotel(data, self.test_file)
        Hotel.modify_hotel(50, self.test_file, name="No Existe")
        hotels = Hotel.load_hotels(self.test_file)
        self.assertEqual(hotels[0].name, "Original")

    def test_cancel_reservation_logic(self):
        """Verifica que cancelar reserva aumente disponibilidad."""
        hotel = Hotel(1, "Test", "Lugar", 5)
        hotel.cancel_reservation(self.test_file)
        self.assertEqual(hotel.rooms, 6)

    def test_display_hotel_not_found(self):
        """Verifica comportamiento cuando no existe el hotel."""
        result = Hotel.display_hotel(999, self.test_file)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
