# Proyecto de Reservas

## Descripción
Este proyecto consiste en una aplicación para gestionar reservas y reseñas en restaurantes. Está implementado en Python y utiliza clases para representar clientes, restaurantes, reservas y reseñas.

## Requisitos

- Python 3.x
- `validators` (instalable mediante `requirements.txt`)

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/usuario/proyecto-reservas.git
    ```

2. Navega al directorio del proyecto:
    ```bash
    cd proyecto-reservas
    ```

3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

### Clases Principales

- **Client**: Representa a un cliente.
- **Restaurant**: Representa a un restaurante.
- **Booking**: Representa una reserva.
- **Review**: Representa una reseña.

### Ejemplo de Uso

A continuación, se muestra un ejemplo de cómo usar las clases y crear instancias:

```python
from Client import Client
from Restaurant import Restaurant
from Booking import Booking
from Review import Review

# Crear un cliente
cliente1 = Client(name="Alberto", surname="Cuadrado", phone="691840868", password="password1", username="UsuarioAlberto")

# Crear un restaurante
restaurante1 = Restaurant(address="Calle Falsa 123", name="El Buen Sabor", password="restpass", locality="Madrid", tables=20)

# Crear una reserva
reserva1 = Booking(clientId=cliente1.id, restaurantId=restaurante1.id, bookedTables=2, date="2024-11-23")

# Añadir la reserva al cliente y al restaurante
cliente1.add_booking(reserva1)
restaurante1.add_booking(reserva1)

# Crear una reseña
review1 = Review(clientId=cliente1.id, restaurantId=restaurante1.id, rating=5, comment="Excelente servicio")

# Añadir la reseña al cliente y al restaurante
cliente1.add_review(review1)
restaurante1.add_review(review1)

# Añadir una imagen al restaurante
restaurante1.add_image("https://example.com/imagen.jpg")
