import customtkinter as ctk
from Controllers import BasicController
from datetime import datetime


class ClientBookingsFrame(ctk.CTkFrame):
    def __init__(self, parent, db, dni):
        super().__init__(parent)
        self.db = db
        self.dni = dni
        self.setup_ui()
        self.load_bookings()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._create_title()
        self._create_bookings_frame()

    def _create_title(self):
        self.title = ctk.CTkLabel(
            self,
            text="Mis Reservas",
            font=("Helvetica", 36, "bold")
        )
        self.title.grid(row=0, column=0, padx=120, pady=(50, 10), sticky="n")

    def _create_bookings_frame(self):
        self.bookings_frame = ctk.CTkScrollableFrame(self, width=400, height=500)
        self.bookings_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.bookings_frame.grid_columnconfigure(0, weight=1)

    def load_bookings(self):
        for widget in self.bookings_frame.winfo_children():
            widget.destroy()

        bookings = self.db.get_client_bookings(self.dni)
        current_time = datetime.now()
        future_bookings = [booking for booking in bookings if booking.date >= current_time]

        if not future_bookings:
            self._show_no_bookings_message()
            return

        for booking in future_bookings:
            self._create_booking_card(booking)

    def _show_no_bookings_message(self):
        message = ctk.CTkLabel(
            self.bookings_frame,
            text="No tienes reservas activas",
            font=("Helvetica", 18)
        )
        message.grid(row=0, column=0, pady=20)

    def _create_booking_card(self, booking):
        restaurant = self.db.obtain_restaurant(booking.restaurantCIF)
        if not restaurant:
            return
        container_frame = ctk.CTkFrame(
            self.bookings_frame,
            corner_radius=10,
            fg_color="black"
        )
        container_frame.grid(sticky="ew", padx=10, pady=10)
        container_frame.grid_columnconfigure(1, weight=1)

        restaurant_info = ctk.CTkLabel(
            container_frame,
            text=f"Restaurante: {restaurant.name}",
            font=("Helvetica", 18, "bold")
        )
        restaurant_info.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        address_info = ctk.CTkLabel(
            container_frame,
            text=f"Dirección: {restaurant.address}",
            font=("Helvetica", 16)
        )
        address_info.grid(row=1, column=0, columnspan=2, padx=10, pady=2, sticky="w")

        date_str = datetime.strftime(booking.date, '%Y-%m-%d %H:%M:%S')

        booking_info = ctk.CTkLabel(
            container_frame,
            text=f"Fecha: {date_str}",
            font=("Helvetica", 16)
        )
        booking_info.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        booking_info2 = ctk.CTkLabel(
            container_frame,
            text=f"Mesas: {booking.bookedTables}",
            font=("Helvetica", 16)
        )
        booking_info2.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        cancel_btn = ctk.CTkButton(
            container_frame,
            text="Cancelar Reserva",
            command=lambda: self._cancel_booking(booking.id),
            fg_color="red",
            hover_color="darkred",
            width=120
        )
        cancel_btn.grid(row=4, column=0, padx=10, pady=10, sticky="w")

    def _cancel_booking(self, booking_id):
        try:
            if self.db.delete_booking(booking_id):
                BasicController.usage_window("Éxito", "Reserva cancelada correctamente")
                self.load_bookings()  # Refresh the bookings list
            else:
                raise Exception("No se pudo cancelar la reserva")
        except Exception as e:
            BasicController.show_errors([f"Error: {str(e)}"])
