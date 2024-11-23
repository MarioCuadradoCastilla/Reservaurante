from datetime import datetime

class Booking:
    def __init__(self,clientDNI, restaurantCIF, bookedTables, date):
        self.id = None
        self.clientDNI =clientDNI
        self.restaurantCIF = restaurantCIF
        self.bookedTables = bookedTables
        self.date = date

    def __repr__(self):
        return (
            f"Booking(clientDNI={self.clientDNI}, restaurantCIF={self.restaurantCIF}, 
            "f"bookedTables={self.bookedTables}, date={self.date})")
        