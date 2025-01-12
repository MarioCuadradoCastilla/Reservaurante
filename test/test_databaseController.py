import unittest
import sqlite3
import os
import shutil
import tempfile
import timeit
from datetime import datetime
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

    def tearDown(self):
        # Eliminar el directorio temporal y cerrar la conexión a la base de datos
        shutil.rmtree(self.test_dir)
        self.conn.close()

    def test_get_available_tables_no_bookings(self):
        date = datetime(2024, 1, 1, 12, 0)

        tiempo = timeit.timeit(lambda: self.controller.get_available_tables('B12345678', date), number=100)
        print(f"Tiempo de ejecución: {tiempo} segundos")

        available_tables = self.controller.get_available_tables('B12345678', date)
        self.assertEqual(available_tables, 10)
        print(f"test_get_available_tables_no_bookings: {available_tables} (Expected: 10)")

    def test_get_available_tables_with_bookings(self):
        date = datetime(2024, 1, 15, 14, 30)

        # Medir el tiempo de ejecución de la función
        tiempo = timeit.timeit(lambda: self.controller.get_available_tables('B12345678', date), number=100)
        print(f"Tiempo de ejecución: {tiempo} segundos")

        available_tables = self.controller.get_available_tables('B12345678', date)
        print(f"MESAS RESERVADAS {date}: {10 - available_tables}")

        # Ajuste en la expectativa del test a 8 mesas disponibles
        self.assertEqual(available_tables, 8)
        print(f"MESAS RECIBIDAS: {available_tables} (MESAS ESPERADAS: 8)")

    def test_get_available_tables_restaurant_not_found(self):
        date = datetime(2024, 1, 1, 12, 0)

        # Medir el tiempo de ejecución de la función
        tiempo = timeit.timeit(lambda: self.controller.get_available_tables('B99999999', date), number=100)
        print(f"Tiempo de ejecución: {tiempo} segundos")

        available_tables = self.controller.get_available_tables('B99999999', date)
        self.assertIsNone(available_tables)
        print(f"test_get_available_tables_restaurant_not_found: {available_tables} (Expected: None)")

    def test_add_restaurant_image_creates_directory(self):
        with tempfile.NamedTemporaryFile(suffix='.jpg') as tmp_file:
            restaurant_cif = 'B12345678'

            # Medir el tiempo de ejecución de la función
            tiempo = timeit.timeit(lambda: self.controller.add_restaurant_image(restaurant_cif, tmp_file.name), number=10)
            print(f"Tiempo de ejecución: {tiempo} segundos")

            self.controller.add_restaurant_image(restaurant_cif, tmp_file.name)
            expected_dir = os.path.join(self.controller.images_dir, restaurant_cif)
            directory_exists = os.path.isdir(expected_dir)
            self.assertTrue(directory_exists)
            print(f"test_add_restaurant_image_creates_directory: {directory_exists} (Expected: True)")

    def test_add_restaurant_image_copies_file(self):
        with tempfile.NamedTemporaryFile(suffix='.jpg') as tmp_file:
            restaurant_cif = 'B12345678'

            # Medir el tiempo de ejecución de la función
            tiempo = timeit.timeit(lambda: self.controller.add_restaurant_image(restaurant_cif, tmp_file.name), number=10)
            print(f"Tiempo de ejecución: {tiempo} segundos")

            new_filename = self.controller.add_restaurant_image(restaurant_cif, tmp_file.name)
            expected_path = os.path.join(self.controller.images_dir, restaurant_cif, new_filename)
            file_exists = os.path.isfile(expected_path)
            self.assertTrue(file_exists)
            print(f"test_add_restaurant_image_copies_file: {file_exists} (Expected: True)")

    @patch('Controllers.DataBaseController.uuid.uuid4')
    def test_add_restaurant_image_filename(self, mock_uuid):
        mock_uuid.return_value.hex = 'test-uuid'
        with tempfile.NamedTemporaryFile(suffix='.jpg') as tmp_file:
            restaurant_cif = 'B12345678'

            # Medir el tiempo de ejecución de la función
            tiempo = timeit.timeit(lambda: self.controller.add_restaurant_image(restaurant_cif, tmp_file.name), number=10)
            print(f"Tiempo de ejecución: {tiempo} segundos")

            new_filename = self.controller.add_restaurant_image(restaurant_cif, tmp_file.name)
            _, ext = os.path.splitext(tmp_file.name)
            expected_filename = f"test-uuid_{int(datetime.now().timestamp())}{ext}"
            self.assertEqual(new_filename, expected_filename)
            print(f"test_add_restaurant_image_filename: {new_filename} (Expected: {expected_filename})")

    def test_add_restaurant_image_db_entry(self):
        with tempfile.NamedTemporaryFile(suffix='.jpg') as tmp_file:
            restaurant_cif = 'B12345678'

            # Medir el tiempo de ejecución de la función
            tiempo = timeit.timeit(lambda: self.controller.add_restaurant_image(restaurant_cif, tmp_file.name), number=10)
            print(f"Tiempo de ejecución: {tiempo} segundos")

            new_filename = self.controller.add_restaurant_image(restaurant_cif, tmp_file.name)
            self.controller.cursor.execute('''
                SELECT * FROM RestaurantImages WHERE restaurantCIF = ? AND filename = ?
            ''', (restaurant_cif, new_filename))
            result = self.controller.cursor.fetchone()
            print(f"test_add_restaurant_image_db_entry: {result} (Expected: Not None)")
            self.assertIsNotNone(result)
            self.assertEqual(result[1], restaurant_cif)
            self.assertEqual(result[2], new_filename)

if __name__ == '__main__':
    unittest.main()
