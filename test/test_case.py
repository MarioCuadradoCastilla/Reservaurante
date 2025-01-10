
from Data.Demo.DemoData import load_demo_data
import unittest
from datetime import datetime
from unittest.mock import Mock, MagicMock
from customtkinter import CTk
from Controllers.DataBaseController import DataBaseController
from Views.ClientApp.Frames.AddBookingFrame import BookingWindow


class TestBookingFunctionality(unittest.TestCase):
    def setUp(self):
        # Crear una instancia real de Tkinter como ventana principal
        self.root = CTk()

        # Crear una instancia mock de la base de datos
        self.db = MagicMock(spec=DataBaseController)
        self.db.cursor = MagicMock()

        # Cargar los datos de demostración en la base de datos mock
        load_demo_data(self.db)

        # Simular datos del restaurante
        self.restaurant_data = {
            'cif': 'B12345678',
            'name': 'El Buen Sabor',
            'address': 'Calle Buenavida 2'
        }
        self.dni = '12345678A'

        # Crear instancia de la ventana de reservas
        self.booking_window = BookingWindow(self.root, self.db, self.restaurant_data, self.dni)

    def tearDown(self):
        # Asegurarse de que no hay eventos pendientes
        self.root.update_idletasks()

        # Cerrar la ventana de Tkinter después de cada prueba
        self.root.destroy()

    def test_make_booking_success(self):
        # Limpiar las llamadas a add_booking antes de la prueba
        self.db.add_booking.reset_mock()

        # Simular la interacción del usuario
        self.booking_window.tables_spinbox.delete(0, "end")
        self.booking_window.tables_spinbox.insert(0, "5")
        self.booking_window.calendar.selection_set(datetime(2024, 1, 1))
        self.booking_window.time_spinboxes[0].delete(0, "end")
        self.booking_window.time_spinboxes[0].insert(0, "12")
        self.booking_window.time_spinboxes[1].delete(0, "end")
        self.booking_window.time_spinboxes[1].insert(0, "00")

        # Ajustar para simular mesas disponibles
        self.db.get_available_tables.return_value = 10

        # Ejecutar la lógica de submit
        self.booking_window._handle_submit()

        # Verificar que la reserva se ha realizado correctamente
        self.db.add_booking.assert_called_once()
        booking_call = self.db.add_booking.call_args[0][0]
        self.assertEqual(booking_call.clientDNI, self.dni)
        self.assertEqual(booking_call.restaurantCIF, self.restaurant_data['cif'])

    def test_make_booking_failure(self):
        # Limpiar las llamadas a add_booking antes de la prueba
        self.db.add_booking.reset_mock()

        # Simular que no hay mesas disponibles
        self.db.get_available_tables.return_value = 0

        # Simular la interacción del usuario
        self.booking_window.tables_spinbox.delete(0, "end")
        self.booking_window.tables_spinbox.insert(0, "20")
        self.booking_window.calendar.selection_set(datetime(2024, 1, 1))
        self.booking_window.time_spinboxes[0].delete(0, "end")
        self.booking_window.time_spinboxes[0].insert(0, "19")
        self.booking_window.time_spinboxes[1].delete(0, "end")
        self.booking_window.time_spinboxes[1].insert(0, "00")

        # Ejecutar la lógica de submit
        self.booking_window._handle_submit()

        # Verificar que no se ha realizado ninguna reserva
        self.db.add_booking.assert_not_called()


if __name__ == '__main__':
    unittest.main()


