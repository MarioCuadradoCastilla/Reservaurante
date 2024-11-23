import sqlite3
from datetime import datetime, timedelta
from Model import Client
from Model import Restaurant
from Model import Booking
from Model import Review

class DataBaseReservaurante:
    def __init__(self, db_path="Reservaurante.db"):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        # Crear tabla Client
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Client (
                dni INTEGER PRIMARY KEY,
                name TEXT,
                surname TEXT,
                phone INTEGER,
                password TEXT,
                username TEXT
            );
        ''')

        # Crear tabla Restaurant
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Restaurant (
                cif INTEGER PRIMARY KEY,
                address TEXT,
                name TEXT,
                password TEXT,
                municipality TEXT,
                tables INTEGER,
                rating REAL
            );
        ''')

        # Crear tabla Bookings
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                clientDNI INTEGER,
                restaurantCIF INTEGER,
                bookedTables INTEGER,
                date DATETIME,
                FOREIGN KEY (clientDNI) REFERENCES Client(dni),
                FOREIGN KEY (restaurantCIF) REFERENCES Restaurant(cif)
            );
        ''')
        
        # Crear tabla Reviews
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                clientDNI INTEGER,
                restaurantCIF INTEGER,
                rating INTEGER,
                comment TEXT,
                date DATETIME,
                FOREIGN KEY (clientDNI) REFERENCES Client(dni),
                FOREIGN KEY (restaurantCIF) REFERENCES Restaurant(cif)
            );
        ''')
        self.connection.commit()

    def add_client(self, client):
        self.cursor.execute('''
            INSERT INTO Client (dni, name, surname, phone, password, username)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (client.dni, client.name, client.surname, client.phone, client.password, client.username))
        self.connection.commit()

    def add_restaurant(self, restaurant):
        self.cursor.execute('''
            INSERT INTO Restaurant (cif, address, name, password, municipality, tables, rating)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (restaurant.cif, restaurant.address, restaurant.name, restaurant.password, restaurant.municipality, restaurant.tables, restaurant.rating))
        self.connection.commit()

    def add_booking(self, booking):
        self.cursor.execute('''
            INSERT INTO Bookings (clientDNI, restaurantCIF, bookedTables, date)
            VALUES (?, ?, ?, ?)
        ''', (booking.clientDNI, booking.restaurantCIF, booking.bookedTables, booking.date))
        self.connection.commit()
        booking.id = self.cursor.lastrowid  # Asigna el ID generado automáticamente

    def add_review(self, review):
        self.cursor.execute('''
            INSERT INTO Reviews (clientDNI, restaurantCIF, rating, comment, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (review.clientDNI, review.restaurantCIF, review.rating, review.comment, review.date))
        self.connection.commit()
        review.id = self.cursor.lastrowid  # Asigna el ID generado automáticamente

    def get_available_tables(self, restaurantCIF, date, reserved_tables):
        """
        Consulta el número de mesas disponibles en un restaurant para una fecha y hora específica.
        """
        self.cursor.execute("SELECT tables FROM Restaurant WHERE cif = ?", (restaurantCIF,))
        result = self.cursor.fetchone()
        if result is None:
            print("Restaurante no encontrado.")
            return None

        total_tables = result[0]
        start_date = date
        finish_date = date + timedelta(hours=2)

        self.cursor.execute('''
            SELECT SUM(bookedTables) 
            FROM Bookings 
            WHERE restaurantCIF = ? 
            AND DATE(date) = DATE(?) 
            AND (
                (date < ? AND datetime(date, '+2 hours') > ?)
                OR
                (date >= ? AND date < ?)
            );
        ''', (restaurantCIF, start_date, finish_date, start_date, start_date, finish_date))

        result_bookings = self.cursor.fetchone()
        reserved_tables = result_bookings[0] if result_bookings[0] else 0

        available_tables = total_tables - reserved_tables
        if available_tables >= reserved_tables:
            print(f"Mesas disponibles: {available_tables}")
            return available_tables
        else:
            print(f"No hay suficientes mesas disponibles. Mesas solicitadas: {reserved_tables}, Mesas disponibles: {available_tables}")
            return available_tables

    def close_connection(self):
        self.connection.close()
