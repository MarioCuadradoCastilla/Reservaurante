from datetime import datetime
from Models.Client import Client
from Models.Restaurant import Restaurant
from Models.Review import Review
from Models.Booking import Booking

def create_datetime(year, month, day, hour=12, minute=0):
    return datetime(year, month, day, hour, minute)

def load_demo_data(db_controller):
    db_controller.cursor.execute("DELETE FROM Client;")
    db_controller.cursor.execute("DELETE FROM Restaurant;")
    db_controller.cursor.execute("DELETE FROM Bookings;")
    db_controller.cursor.execute("DELETE FROM Reviews;")
    # Demo Clients
    clients = [
        Client("12345678A", "John", "Doe", 123456789, "Pass123@", "john_doe"),
        Client("87654321B", "Jane", "Smith", 987654321, "Smith2#", "jane_smith"),
        Client("11111111C", "Alice", "Johnson", 555555555, "Alice3$", "alice_j"),
        Client("22222222D", "Bob", "Wilson", 444444444, "Wilson4€", "bob_w"),
        Client("33333333E", "Carol", "Brown", 333333333, "Brown5@", "carol_b"),
        Client("44444444F", "David", "Miller", 666666666, "Miller6#", "david_m"),
        Client("55555555G", "Emma", "Davis", 777777777, "Davis7$", "emma_d"),
        Client("66666666H", "Frank", "Taylor", 888888888, "Taylor8€", "frank_t"),
        Client("77777777I", "Grace", "Anderson", 999999999, "Anders9@", "grace_a"),
        Client("88888888J", "Henry", "Moore", 111111111, "Moore10#", "henry_m")
    ]

    for client in clients:
        if not db_controller.check_username_exists(client.username):
            db_controller.add_client(client)

    restaurants = [
        Restaurant("B12345678", "Calle Buenavida 2", "El Buen Sabor", "Lugar123@", "La Acebeda", 10, 111222333,
                   "Un acogedor restaurante en La Acebeda, perfecto para disfrutar de la gastronomía local."),
        Restaurant("B23456789", "Calle de los Sabores 5", "Sabores y Tradición", "Sabores456@", "Ajalvir", 20,
                   222333444, "Un rincón ideal en Ajalvir para deleitarse con sabores exquisitos."),
        Restaurant("B34567890", "Avenida del Valle 12", "La Delicia del Valle", "Delicias789@", "Alameda del Valle", 15,
                   333444555, "Famoso en Alameda del Valle por sus recetas tradicionales con un toque moderno."),
        Restaurant("B45678901", "Plaza Principal 1", "Sabor y Arte", "CasaSabor012@", "El Álamo", 25, 444555666,
                   "Situado en El Álamo, ofrece una experiencia gastronómica inolvidable."),
        Restaurant("B56789012", "Calle del Patrimonio 8", "El Palacio del Sabor", "Sabores345@", "Alcalá de Henares",
                   18, 555666777, "Un restaurante en Alcalá de Henares que combina historia y buena comida."),
        Restaurant("B67890123", "Avenida de la Comida 3", "La Cocina de la Abuela", "Comida678@", "Alcobendas", 12,
                   666777888, "Popular en Alcobendas por su ambiente acogedor y platos caseros."),
        Restaurant("B78901234", "Calle del Rincón 7", "El Rincón del Chef", "Rincon901@", "Alcorcón", 22, 777888999,
                   "Reconocido en Alcorcón por su menú innovador y servicio excelente."),
        Restaurant("B89012345", "Calle Mágica 9", "La Mesa de los Sabores", "Aldea234@", "Aldea del Fresno", 10,
                   888999000, "Ubicado en Aldea del Fresno, ideal para los amantes de la buena mesa."),
        Restaurant("B90123456", "Calle del Norte 4", "La Ruta del Norte", "Sabores567@", "Algete", 14, 999000111,
                   "Especializado en cocina norteña, este restaurante en Algete es un favorito."),
        Restaurant("B01234567", "Calle Piedra Dorada 6", "El Sabor Dorado", "Piedra890@", "Alpedrete", 16, 123456789,
                   "Un encantador restaurante en Alpedrete con una amplia variedad de platos.")
    ]

    def get_restaurant_address_by_cif(cif):
        for restaurant in restaurants:
            if restaurant.cif == cif:
                return restaurant.address
        return None

    for restaurant in restaurants:
        db_controller.add_restaurant(restaurant)

    # Demo Bookings con fechas específicas
    bookings = [
        Booking(1, "12345678A", "B12345678", 2, get_restaurant_address_by_cif("B12345678"),
                create_datetime(2024, 1, 15, 14, 30)),
        Booking(2, "87654321B", "B23456789", 4, get_restaurant_address_by_cif("B23456789"),
                create_datetime(2024, 1, 16, 20, 0)),
        Booking(3, "11111111C", "B34567890", 3, get_restaurant_address_by_cif("B34567890"),
                create_datetime(2024, 1, 17, 13, 0)),
        Booking(4, "22222222D", "B45678901", 2, get_restaurant_address_by_cif("B45678901"),
                create_datetime(2024, 1, 18, 19, 30)),
        Booking(5, "33333333E", "B56789012", 5, get_restaurant_address_by_cif("B56789012"),
                create_datetime(2024, 1, 19, 21, 0)),

        Booking(6, "44444444F", "B12345678", 3, get_restaurant_address_by_cif("B12345678"),
                create_datetime(2024, 2, 1, 18, 30)),
        Booking(7, "55555555G", "B23456789", 2, get_restaurant_address_by_cif("B23456789"),
                create_datetime(2024, 2, 2, 20, 30)),
        Booking(8, "66666666H", "B34567890", 4, get_restaurant_address_by_cif("B34567890"),
                create_datetime(2024, 2, 3, 19, 0)),
        Booking(9, "77777777I", "B45678901", 6, get_restaurant_address_by_cif("B45678901"),
                create_datetime(2024, 2, 4, 14, 0)),
        Booking(10, "88888888J", "B56789012", 2, get_restaurant_address_by_cif("B56789012"),
                create_datetime(2024, 2, 5, 21, 30)),

        Booking(11, "12345678A", "B23456789", 3, get_restaurant_address_by_cif("B23456789"),
                create_datetime(2024, 3, 5, 13, 30)),
        Booking(12, "87654321B", "B34567890", 2, get_restaurant_address_by_cif("B34567890"),
                create_datetime(2024, 3, 6, 20, 0)),
        Booking(13, "11111111C", "B45678901", 4, get_restaurant_address_by_cif("B45678901"),
                create_datetime(2024, 3, 7, 19, 30)),
        Booking(14, "22222222D", "B56789012", 3, get_restaurant_address_by_cif("B56789012"),
                create_datetime(2024, 3, 8, 18, 0)),
        Booking(15, "33333333E", "B12345678", 2, get_restaurant_address_by_cif("B12345678"),
                create_datetime(2024, 3, 9, 21, 0)),

        Booking(16, "55555555G", "B67890123", 2, get_restaurant_address_by_cif("B67890123"),
                create_datetime(2024, 3, 10, 19, 0)),
        Booking(17, "44444444F", "B78901234", 4, get_restaurant_address_by_cif("B78901234"),
                create_datetime(2024, 3, 11, 20, 0)),
        Booking(18, "77777777I", "B89012345", 3, get_restaurant_address_by_cif("B89012345"),
                create_datetime(2024, 3, 12, 21, 0)),
        Booking(19, "88888888J", "B90123456", 2, get_restaurant_address_by_cif("B90123456"),
                create_datetime(2024, 3, 13, 22, 0)),
        Booking(20, "66666666H", "B01234567", 2, get_restaurant_address_by_cif("B01234567"),
                create_datetime(2024, 3, 14, 19, 0))
    ]

    for booking in bookings:
        db_controller.add_booking(booking)

    # Demo Reviews con fechas específicas
    reviews = [
        # Reseñas para "El Buen Lugar"
        Review("12345678A", "john_doe", "B12345678", 4.5, "¡Excelente comida y servicio!", create_datetime(2023, 12, 1, 22, 0)),
        Review("33333333E", "carol_b", "B12345678", 4.2, "Una velada encantadora", create_datetime(2024, 1, 10, 21, 0)),
        Review("55555555G", "emma_d", "B12345678", 4.0, "Buen lugar para compartir", create_datetime(2024, 2, 15, 20, 0)),

        # Reseñas para "Sabores Únicos"
        Review("87654321B", "jane_smith", "B23456789", 4.0, "Buen ambiente", create_datetime(2023, 12, 2, 23, 0)),
        Review("55555555G", "emma_d", "B23456789", 3.8, "Buena relación calidad-precio", create_datetime(2024, 1, 2, 22, 0)),
        Review("12345678A", "john_doe", "B23456789", 4.1, "Buena comida y ambiente agradable", create_datetime(2024, 3, 5, 14, 0)),

        # Reseñas para "Delicias del Valle"
        Review("11111111C", "alice_j", "B34567890", 4.8, "Experiencia increíble", create_datetime(2023, 12, 3, 22, 30)),
        Review("66666666H", "frank_t", "B34567890", 4.6, "¡Sabores increíbles!", create_datetime(2024, 1, 3, 21, 30)),
        Review("87654321B", "jane_smith", "B34567890", 4.2, "Un lugar especial", create_datetime(2024, 3, 6, 20, 30)),

        # Reseñas para "La Casa del Sabor"
        Review("22222222D", "bob_w", "B45678901", 3.5, "Buena comida pero servicio lento", create_datetime(2023, 12, 4, 21, 0)),
        Review("77777777I", "grace_a", "B45678901", 4.3, "Personal amable y ambiente acogedor", create_datetime(2024, 1, 4, 22, 30)),
        Review("11111111C", "alice_j", "B45678901", 4.0, "Buena opción para cenas familiares", create_datetime(2024, 3, 7, 20, 0)),

        # Reseñas para "Sabores del Patrimonio"
        Review("33333333E", "carol_b", "B56789012", 5.0, "¡Perfecto en todo!", create_datetime(2023, 12, 5, 22, 30)),
        Review("88888888J", "henry_m", "B56789012", 4.7, "¡Volveré seguro!", create_datetime(2024, 1, 5, 23, 0)),
        Review("22222222D", "bob_w", "B56789012", 4.5, "Una experiencia memorable", create_datetime(2024, 3, 8, 21, 0)),

        # Más reseñas adicionales por cliente para cumplir requisitos
        Review("44444444F", "david_m", "B67890123", 4.2, "Gran ambiente y buena comida", create_datetime(2024, 2, 15, 22, 0)),
        Review("44444444F", "david_m", "B78901234", 4.4, "Servicio excelente y menú innovador", create_datetime(2024, 3, 11, 20, 30)),
        Review("88888888J", "henry_m", "B90123456", 4.8, "Cocina increíble", create_datetime(2024, 3, 13, 22, 30))
    ]

    for review in reviews:
        db_controller.add_review(review)

if __name__ == "__main__":
    from Controllers.DataBaseController import DataBaseController

    db = DataBaseController()
    load_demo_data(db)
