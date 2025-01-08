from .Booking import Booking
from .Review import Review
import validators
import os
from pathlib import Path


class Restaurant:
    def __init__(self, cif, address, name, password, municipality, tables, phone,description):
        self.cif = cif
        self.address = address
        self.name = name
        self.password = password
        self.municipality = municipality
        self.tables = tables
        self.description=description
        self.bookings = []
        self.reviews = []
        self.images = []
        self.phone = phone

    def add_booking(self, booking):
        if isinstance(booking, Booking):
            self.bookings.append(booking)
        else:
            raise TypeError("Expected an instance of Booking")

    def add_review(self, review):
        if isinstance(review, Review):
            self.reviews.append(review)
        else:
            raise TypeError("Expected an instance of Review")

    def add_image(self, image_path):
        if not os.path.isfile(image_path):
            raise ValueError("Invalid image file")

        original_name = Path(image_path).stem
        extension = Path(image_path).suffix
        new_filename = f"{original_name}_{self.cif}{extension}"
        self.images.append(new_filename)
        return new_filename

