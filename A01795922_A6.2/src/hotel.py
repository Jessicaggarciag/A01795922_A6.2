"""Módulo para la gestión de hoteles y persistencia en JSON."""
import json
import os


class Hotel:
    """Clase para representar y gestionar un Hotel."""

    def __init__(self, hotel_id, name, location, rooms):
        """Inicializa los atributos del hotel."""
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.rooms = rooms

    def to_dict(self):
        """Convierte la instancia a diccionario."""
        return self.__dict__

    @classmethod
    def create_hotel(cls, hotel_id, name, location, rooms, filename):
        """Crea un hotel y lo guarda en el archivo JSON."""
        hotels = cls.load_hotels(filename)
        new_hotel = cls(hotel_id, name, location, rooms)
        hotels.append(new_hotel)
        cls.save_to_file(filename, hotels)
        return new_hotel

    @staticmethod
    def delete_hotel(hotel_id, filename):
        """Elimina un hotel por su ID."""
        hotels = Hotel.load_hotels(filename)
        updated_hotels = [h for h in hotels if h.hotel_id != hotel_id]
        Hotel.save_to_file(filename, updated_hotels)

    @staticmethod
    def display_hotel(hotel_id, filename):
        """Muestra la información de un hotel específico."""
        hotels = Hotel.load_hotels(filename)
        for hotel in hotels:
            if hotel.hotel_id == hotel_id:
                print(f"ID: {hotel.hotel_id} | Nombre: {hotel.name} "
                      f"| Ubicación: {hotel.location} | Cuartos: {hotel.rooms}")
                return hotel
        print("Hotel no encontrado.")
        return None

    @staticmethod
    def modify_hotel(hotel_id, filename, **kwargs):
        """Modifica la información de un hotel existente."""
        hotels = Hotel.load_hotels(filename)
        for hotel in hotels:
            if hotel.hotel_id == hotel_id:
                hotel.name = kwargs.get('name', hotel.name)
                hotel.location = kwargs.get('location', hotel.location)
                hotel.rooms = kwargs.get('rooms', hotel.rooms)
                break
        Hotel.save_to_file(filename, hotels)

    def reserve_room(self, filename):
        """Reduce la disponibilidad de cuartos."""
        if self.rooms > 0:
            self.rooms -= 1
            Hotel.modify_hotel(self.hotel_id, filename, rooms=self.rooms)
            return True
        print("No hay habitaciones disponibles.")
        return False

    def cancel_reservation(self, filename):
        """Aumenta la disponibilidad de cuartos."""
        self.rooms += 1
        Hotel.modify_hotel(self.hotel_id, filename, rooms=self.rooms)

    @staticmethod
    def load_hotels(filename):
        """Carga hoteles manejando datos inválidos."""
        if not os.path.exists(filename):
            return []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [Hotel(**h) for h in data]
        except (json.JSONDecodeError, TypeError, KeyError) as error:
            print(f"Error de datos: {error}")  # Req 5: Continúa la ejecución
            return []

    @staticmethod
    def save_to_file(filename, hotels):
        """Guarda la lista en el archivo persistente."""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump([h.to_dict() for h in hotels], file, indent=4)
        except IOError as error:
            print(f"Error al guardar: {error}")
