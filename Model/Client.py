class Client:
    def __init__(self,dni,name, surname, phone, password, username):
        self.dni = dni
        self.name = name
        self.surname = surname
        self.phone = phone
        self.password = password
        self.username = username
        self.bookings = []
        self.reviews = []

    def add_booking(self, booking):
        self.bookings.append(booking)

    def add_review(self, review):
        self.reviews.append(review)
