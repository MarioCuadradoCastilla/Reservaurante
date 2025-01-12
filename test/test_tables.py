import unittest
import sqlite3
import os
import shutil
import tempfile
import timeit
from datetime import datetime, timedelta
from Controllers.DataBaseController import DataBaseController
from Data.Demo.DemoData import load_demo_data
from unittest.mock import patch

class TestDataBaseController(unittest.TestCase):
    def setUp(self):
        # Usar una base de datos en memoria para las pruebas
        self.conn = sqlite3.connect(':memory:')
        self.controller = DataBaseController(db_path=':memory:')
        self.controller.connection = self.conn
        self.controller.cursor = self.conn.cursor()
        self.controller.create_tables_if_not_exists()

        # Crear un directorio temporal para las imágenes
        self.test_dir = tempfile.mkdtemp()
        self.controller.images_dir = self.test_dir

        # Cargar los datos de demo
        load_demo_data(self.controller)

    def test_get_available_tables_with_bookings(self):
        date = datetime(2025, 1, 15, 14, 30)

        # Medir el tiempo de ejecución de la función
        #tiempo = timeit.timeit(lambda: self.controller.get_available_tables('B12345678', date), number=100)
        #print(f"Tiempo de ejecución: {tiempo} segundos")

        # Llamar a la función solo una vez y guardar el resultado
        available_tables = self.controller.get_available_tables('B12345678', date)
        print(f"MESAS RESERVADAS {date}: {10 - available_tables}")

        # La expectativa correcta es 8 mesas disponibles
        self.assertEqual(8, available_tables)
        print(f"MESAS RECIBIDAS: {available_tables} (MESAS ESPERADAS: 8)")

    def tearDown(self):
        # Eliminar el directorio temporal y cerrar la conexión a la base de datos
        shutil.rmtree(self.test_dir)
        self.conn.close()

if __name__ == '__main__':
    unittest.main()
