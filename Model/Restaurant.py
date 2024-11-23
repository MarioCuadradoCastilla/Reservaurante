from Booking import Booking
from Review import Review
import validators
class Restaurant:
    def __init__(self, cif,address, name, password, municipality, tables, rating):
        self.cif = cif
        self.address = address
        self.name = name
        self.password = password
        self.municipality = municipality
        self.tables = tables
        self.bookings = []
        self.reviews = []
        self.images = []
        self.rating=rating
        
    def add_booking(self, booking):
        if isinstance(booking,Booking):
            self.bookings.append(booking)
        else:
            raise TypeError("Excepted an instance of Booking")

    def add_review(self, review):
        if isinstance(review,Review):
            self.reviews.append(review)
        else:
            raise TypeError("Excepted an instance of Booking")
    def add_image(self, image_url): 
        if validators.url(image_url):
            self.images.append(image_url) 
        else: 
            raise ValueError("Invalid URL")
        
