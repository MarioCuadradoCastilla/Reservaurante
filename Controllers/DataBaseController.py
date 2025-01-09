import sqlite3
from datetime import datetime, timedelta
from unittest import result
from Models import Client, Restaurant, Booking, Review
import os
import shutil
import uuid
from pathlib import Path


class DataBaseController:
    def __init__(self, db_path=None):
        if db_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(script_dir, "..", "Data", "DataBase", "Reservaurante.db")

        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_tables_if_not_exists()
        self.path = db_path


        self.images_dir = os.path.join(os.path.dirname(db_path), "restaurant_images")
        os.makedirs(self.images_dir, exist_ok=True)

    def create_tables_if_not_exists(self):
        tables = {
            "Client": '''
                CREATE TABLE IF NOT EXISTS Client (
                    dni TEXT PRIMARY KEY,
                    name TEXT,
                    surname TEXT,
                    phone INTEGER,
                    password TEXT,
                    username TEXT UNIQUE
                )
            ''',
            "Restaurant": '''
                CREATE TABLE IF NOT EXISTS Restaurant (
                    cif TEXT PRIMARY KEY,
                    address TEXT,
                    name TEXT,
                    password TEXT,
                    municipality TEXT,
                    tables INTEGER,
                    phone INTEGER,
                    description TEXT DEFAULT ''
                )
            ''',
            "Bookings": '''
                CREATE TABLE IF NOT EXISTS Bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    clientDNI TEXT,
                    restaurantCIF TEXT,
                    bookedTables INTEGER,
                    restaurantAddress TEXT,
                    date DATETIME,
                    FOREIGN KEY (clientDNI) REFERENCES Client(dni),
                    FOREIGN KEY (restaurantCIF) REFERENCES Restaurant(cif),
                    FOREIGN KEY (restaurantAddress) REFERENCES Restaurant(address)
                )
            ''',
            "Reviews": '''
                CREATE TABLE IF NOT EXISTS Reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    clientDNI TEXT,
                    clientUsername TEXT,
                    restaurantCIF TEXT,
                    rating REAL,
                    comment TEXT,
                    date DATETIME,
                    FOREIGN KEY (clientDNI) REFERENCES Client(dni),
                    FOREIGN KEY (clientUsername) REFERENCES Client(username),
                    FOREIGN KEY (restaurantCIF) REFERENCES Restaurant(cif)
                )
            ''',
            "RestaurantImages": '''
                CREATE TABLE IF NOT EXISTS RestaurantImages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    restaurantCIF TEXT,
                    filename TEXT,
                    upload_date DATETIME,
                    FOREIGN KEY (restaurantCIF) REFERENCES Restaurant(cif)
                )
            '''
        }

        for table_name, create_statement in tables.items():
            self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            if not self.cursor.fetchone():
                self.cursor.execute(create_statement)
        self.connection.commit()

    def add_client(self, Client):
        self.cursor.execute('''
            INSERT INTO Client (dni, name, surname, phone, password, username)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (Client.dni, Client.name, Client.surname, Client.phone, Client.password, Client.username))
        self.connection.commit()

    def add_restaurant(self, Restaurant):
        self.cursor.execute('''
            INSERT INTO Restaurant (cif, address, name, password, municipality, tables, phone, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (Restaurant.cif, Restaurant.address, Restaurant.name, Restaurant.password,
              Restaurant.municipality, Restaurant.tables, Restaurant.phone, Restaurant.description))
        self.connection.commit()

    def add_booking(self, Booking):
        self.cursor.execute('''
            INSERT INTO Bookings (clientDNI, restaurantCIF, bookedTables, restaurantAddress, date)
            VALUES (?, ?, ?, ?,?)
        ''', (Booking.clientDNI, Booking.restaurantCIF, Booking.bookedTables,Booking.restaurantAddress, Booking.date))
        self.connection.commit()
        Booking.id = self.cursor.lastrowid

    def add_review(self, Review):
        self.cursor.execute('''
            INSERT INTO Reviews (clientDNI, clientUsername, restaurantCIF, rating, comment, date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (Review.clientDNI, Review.clientUsername, Review.restaurantCIF,
              Review.rating, Review.comment, Review.date))
        self.connection.commit()
        Review.id = self.cursor.lastrowid

    def add_restaurant_image(self, restaurant_cif,image_path):

        _, ext = os.path.splitext(image_path)
        new_filename = f"{uuid.uuid4().hex}_{int(datetime.now().timestamp())}{ext}"

        restaurant_dir = os.path.join(self.images_dir, restaurant_cif)
        os.makedirs(restaurant_dir, exist_ok=True)

        destination = os.path.join(restaurant_dir, new_filename)
        shutil.copy2(image_path, destination)

        self.cursor.execute('''
            INSERT INTO RestaurantImages (restaurantCIF, filename, upload_date)
            VALUES (?, ?, ?)
        ''', (restaurant_cif, new_filename, datetime.now()))

        self.connection.commit()
        return new_filename

    def delete_restaurant_image(self, restaurant_cif, filename):
        self.cursor.execute('''
            DELETE FROM RestaurantImages
            WHERE restaurantCIF = ? AND filename = ?
        ''', (restaurant_cif, filename))

        self.connection.commit()
        return True
    def delete_booking(self, id_booking):
        # Eliminar la referencia en la base de datos
        self.cursor.execute('''
            DELETE FROM Bookings
            WHERE id = ?
        ''', (id_booking,))

        self.connection.commit()
        return True

    def delete_review(self, review_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM Reviews WHERE id = ?", (review_id,))
        self.connection.commit()
        return True

    def check_username_exists(self, username):
        self.cursor.execute("SELECT username FROM Client WHERE username = ?", (username,))
        result = self.cursor.fetchone()
        return result is not None

    def get_user_name(self, dni):
        self.cursor.execute("SELECT username FROM Client WHERE dni = ?", (dni,))
        result = self.cursor.fetchone()
        if result:
            return result[0]  # Devuelve el primer elemento de la tupla, que debería ser el nombre de usuario
        return None  # Devuelve None si no se encuentra el usuario

    def get_restaurant_images(self, restaurant_cif):

        self.cursor.execute('''
            SELECT filename
            FROM RestaurantImages
            WHERE restaurantCIF = ?
            ORDER BY upload_date DESC
        ''', (restaurant_cif,))

        return self.cursor.fetchall()

    def get_available_tables(self, restaurantCIF, date, reserved_tables):
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
                OR (date >= ? AND date < ?)
            );
        ''', (restaurantCIF, start_date, finish_date, start_date, start_date, finish_date))

        result_Bookings = self.cursor.fetchone()
        reserved_tables = result_Bookings[0] if result_Bookings[0] else 0
        available_tables = total_tables - reserved_tables

        if available_tables >= reserved_tables:
            print(f"Mesas disponibles: {available_tables}")
            return available_tables
        else:
            print(
                f"No hay suficientes mesas disponibles. Mesas solicitadas: {reserved_tables}, Mesas disponibles: {available_tables}")
            return available_tables

    def obtain_dni(self, dni):
        self.cursor.execute("SELECT dni FROM Client WHERE dni = ?", (dni,))
        result = self.cursor.fetchone()
        return False if result is None else True

    def obtain_client_username(self, username):
        self.cursor.execute("SELECT username FROM Client WHERE username = ?", (username,))
        result = self.cursor.fetchone()
        return False if result is None else True

    def obtain_password_client(self, dni):
        self.cursor.execute("SELECT password FROM Client WHERE dni = ?", (dni,))
        data = self.cursor.fetchone()
        return "Este usuario no existe" if data is None else data[0]

    def obtain_restaurant(self, cif):
        self.cursor.execute("SELECT * FROM Restaurant WHERE cif = ?", (cif,))
        result = self.cursor.fetchone()
        if result is None:
            return None
        restaurant = Restaurant(
            cif=result[0],
            address=result[1],
            name=result[2],
            password=result[3],
            municipality=result[4],
            tables=result[5],
            phone=result[6],
            description=result[7]
        )
        return restaurant

    def obtain_restaurant_name(self, name):
        query = "SELECT name FROM Restaurant WHERE name = ?"
        self.cursor.execute(query, (name,))
        result = self.cursor.fetchone()
        return result is not None

    def obtain_client(self, dni):
        self.cursor.execute("SELECT * FROM Client WHERE dni = ?", (dni,))
        result = self.cursor.fetchone()
        if result is None:
            return None
        client = Client(
            dni=result[0],
            name=result[1],
            surname=result[2],
            phone=result[3],
            password=result[4],
            username=result[5],
        )
        return client

    def update_restaurant(self, restaurant):
        try:
            self.cursor.execute('''
                UPDATE Restaurant 
                SET name = ?, address = ?,municipality = ?,tables = ?,phone = ?, description = ?
                WHERE cif = ?
            ''', (restaurant.name,restaurant.address,restaurant.municipality,restaurant.tables,restaurant.phone,restaurant.description,restaurant.cif
            ))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating restaurant: {e}")
            self.connection.rollback()
            return False
    def update_client(self, client):
        try:
            self.cursor.execute('''
                UPDATE Client
                SET name = ?, surname = ?,phone = ?,password = ?,username = ?
                WHERE dni = ?
            ''', (client.name,client.surname,client.phone,client.password,client.username,client.dni
            ))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating restaurant: {e}")
            self.connection.rollback()
            return False

    def obtain_cif(self, cif):
        self.cursor.execute("SELECT cif FROM Restaurant WHERE cif = ?", (cif,))
        result = self.cursor.fetchone()
        return False if result is None else True

    def obtain_password_restaurant(self, cif):
        self.cursor.execute("SELECT password FROM Restaurant WHERE cif = ?", (cif,))
        data = self.cursor.fetchone()
        return "Este restaurante no existe" if data is None else data[0]

    def calculate_restaurant_rating(self, restaurantCIF):

        self.cursor.execute('''
            SELECT AVG(rating)
            FROM Reviews
            WHERE restaurantCIF = ?
        ''', (restaurantCIF,))
        result = self.cursor.fetchone()

        return 0 if result[0] is None else result[0]

    def get_restaurant_bookings(self, restaurant_cif):
        self.cursor.execute('''
            SELECT b.clientDNI, b.date, b.bookedTables,b.id
            FROM Bookings b
            WHERE b.restaurantCIF = ?
            ORDER BY b.date ASC 
        ''', (restaurant_cif,))

        return self.cursor.fetchall()

    def get_client_bookings(self, dni):
        self.cursor.execute('''
            SELECT id, clientDNI, restaurantCIF, bookedTables, restaurantAddress, date
            FROM Bookings
            WHERE clientDNI = ?
            ORDER BY date ASC
        ''', (dni,))
        rows = self.cursor.fetchall()

        bookings = []
        for row in rows:
            bookings.append(Booking(
                id=row[0],
                clientDNI=row[1],
                restaurantCIF=row[2],
                bookedTables=row[3],
                restaurantAddress=row[4],
                date=datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S")
            ))
        return bookings

    def get_restaurant_reviews(self, restaurant_cif):
        self.cursor.execute('''
            SELECT clientDNI, clientUsername, restaurantCIF, rating, comment, date
            FROM Reviews
            WHERE restaurantCIF = ?
            ORDER BY date DESC
        ''', (restaurant_cif,))

        reviews = self.cursor.fetchall()
        return reviews

    def get_client_reviews(self, dni):
        query = '''
            SELECT r.id, r.clientDNI, c.username, r.restaurantCIF, r.rating, r.comment, r.date, res.name 
            FROM Reviews r 
            JOIN Client c ON r.clientDNI = c.dni 
            JOIN Restaurant res ON r.restaurantCIF = res.cif 
            WHERE r.clientDNI = ? 
            ORDER BY r.date DESC
        '''
        self.cursor.execute(query, (dni,))
        reviews = self.cursor.fetchall()
        return reviews

    def open_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None
