class Review:
    def __init__(self,clientDNI,clientUsername, restaurantCIF, rating, comment,date):
        self.id = None
        self.clientDNI =clientDNI
        self.clientUsername = clientUsername
        self.restaurantCIF = restaurantCIF
        self.rating = rating
        self.comment = comment
        self.date = date

