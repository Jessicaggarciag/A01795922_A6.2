# pylint: disable=duplicate-code
"""Módulo para la gestión de reservaciones"""
import json
import os


class Reservation:
    """Clase que representa una Reservación."""

    def __init__(self, reservation_id, customer_id, hotel_id):
        """Inicializa los atributos de la reservación."""
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id

    def to_dict(self):
        """Convierte la instancia a diccionario para JSON."""
        return self.__dict__

    @classmethod
    def create_reservation(cls, data, filename):
        """Crea una reservación y la guarda"""
        reservations = cls.load_reservations(filename)
        new_res = cls(
            data['reservation_id'],
            data['customer_id'],
            data['hotel_id']
        )
        reservations.append(new_res)
        cls.save_to_file(filename, reservations)
        return new_res

    @staticmethod
    def cancel_reservation(res_id, filename):
        """Elimina una reservación del sistema."""
        reservations = Reservation.load_reservations(filename)
        updated = [r for r in reservations if r.reservation_id != res_id]
        Reservation.save_to_file(filename, updated)

    @staticmethod
    def load_reservations(filename):
        """Carga reservaciones desde un archivo JSON."""
        if not os.path.exists(filename):
            return []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [Reservation(**r) for r in data]
        except (json.JSONDecodeError, TypeError, KeyError) as error:
            print(f"Error en reservaciones: {error}")
            return []

    @staticmethod
    def save_to_file(filename, reservations):
        """Guarda la lista de reservaciones en disco."""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump([r.to_dict() for r in reservations], file, indent=4)
        except IOError as error:
            print(f"Error al guardar reservaciones: {error}")
