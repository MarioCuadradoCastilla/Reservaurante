class Review:
    def __init__(self,clientDNI, restaurantCIF, rating, comment,date):
        self.id = None
        self.clientDNI =clientDNI
        self.restaurantCIF = restaurantCIF
        self.rating = rating
        self.comment = comment
        self.date = date

    def __repr__(self):
        return (
            f"Review(clientDNI={self.clientDNI}, restaurantCIF={self.restaurantCIF}, "
            f"rating={self.rating}, comment={self.comment},date = {self.date})"
        )
