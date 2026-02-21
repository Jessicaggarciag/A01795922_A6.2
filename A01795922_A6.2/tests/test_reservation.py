import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.reservation import Reservation

class TestReservation(unittest.TestCase):
    def setUp(self):
        self.test_file = "data/test_reservations.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_create_reservation_success(self):
        """Verifica la creación de reservación."""
        data = {"reservation_id": 500, "customer_id": 101, "hotel_id": 1}
        res = Reservation.create_reservation(data, self.test_file)
        self.assertEqual(res.reservation_id, 500)

    def test_cancel_reservation_success(self):
        """Verifica la cancelación de reservación."""
        data = {"reservation_id": 500, "customer_id": 101, "hotel_id": 1}
        Reservation.create_reservation(data, self.test_file)
        Reservation.cancel_reservation(500, self.test_file)
        self.assertEqual(len(Reservation.load_reservations(self.test_file)), 0)
