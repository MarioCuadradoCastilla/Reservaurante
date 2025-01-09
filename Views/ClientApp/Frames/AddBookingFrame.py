import customtkinter as ctk
from tkinter import Spinbox
from tkcalendar import Calendar
from datetime import datetime
from Controllers import BasicController
from Models.Booking import Booking
from Controllers.BasicController import BasicController as bc


class BookingWindow:
    def __init__(self, parent, db, restaurant_data, dni, bookings_frame=None):
        self.window = ctk.CTkToplevel(parent)
        self.window.title(f"Reserva - {restaurant_data['name']}")
        bc.center_window(self.window, 400, 440)

        self.db = db
        self.restaurant_data = restaurant_data
        self.dni = dni
        self.bookings_frame = bookings_frame

        self.window.grab_set()
        self._init_ui()

    def _init_ui(self):
        # Title
        title = ctk.CTkLabel(
            self.window,
            text="Nueva Reserva",
            font=("Helvetica", 20, "bold")
        )
        title.pack(pady=20)

        # Tables input
        tables_frame = ctk.CTkFrame(self.window)
        tables_frame.pack(fill="x", padx=20, pady=10)

        tables_label = ctk.CTkLabel(tables_frame, text="Número de personas:")
        tables_label.pack(side="left", padx=5)

        self.tables_spinbox = Spinbox(tables_frame, from_=1, to=100, font=("Helvetica", 14))
        self.tables_spinbox.pack(side="right", expand=True, fill="x", padx=5)

        # Date picker
        date_frame = ctk.CTkFrame(self.window)
        date_frame.pack(fill="x", padx=20, pady=10)

        date_label = ctk.CTkLabel(date_frame, text="Fecha:")
        date_label.pack(side="left", padx=5)

        today = datetime.now()
        self.calendar = Calendar(date_frame, selectmode='day', date_pattern='dd/mm/yyyy', mindate=today)
        self.calendar.pack(side="right", expand=True, fill="x", padx=5)

        # Time picker frame
        time_frame = ctk.CTkFrame(self.window)
        time_frame.pack(fill="x", padx=20, pady=10)

        time_label = ctk.CTkLabel(time_frame, text="Hora:")
        time_label.pack(side="left", padx=5)

        hour_spinbox = Spinbox(time_frame, from_=8, to=22, wrap=True, width=3,
                               font=("Helvetica", 14), format="%02.0f")
        hour_spinbox.pack(side="left", padx=5)

        minute_spinbox = Spinbox(time_frame, from_=0, to=59, wrap=True, width=3,
                                 font=("Helvetica", 14), format="%02.0f")
        minute_spinbox.pack(side="left", padx=5)

        self.time_spinboxes = (hour_spinbox, minute_spinbox)

        # Submit button
        submit_btn = ctk.CTkButton(
            self.window,
            text="Confirmar Reserva",
            command=self._handle_submit
        )
        submit_btn.pack(pady=20)

    def _check_availability(self, date, requested_tables):
        return self.db.get_available_tables(
            self.restaurant_data['cif'],
            date,
            requested_tables
        )


    def _make_booking(self, tables, date):
        messages = []
        try:
            booking = Booking(
                id=None,
                clientDNI=self.dni,
                restaurantCIF=self.restaurant_data['cif'],
                bookedTables=tables,
                restaurantAddress=self.restaurant_data['address'],
                date=date
            )

            self.db.add_booking(booking)
            bc.usage_window("Exito", "¡Reserva realizada con éxito!")
            self.window.after(1000, self.window.destroy)

            if self.bookings_frame:
                self.bookings_frame.load_bookings()

        except Exception as e:
            messages.append(f"Error al realizar la reserva: {str(e)}")
            bc.show_errors(messages)

    def _handle_submit(self):
        messages = []
        try:
            num_personas = int(self.tables_spinbox.get())
            date_str = f"{self.calendar.get_date()} {self.time_spinboxes[0].get()}:{self.time_spinboxes[1].get()}"
            date = datetime.strptime(date_str, '%d/%m/%Y %H:%M')

            mesas = num_personas // 4
            if num_personas % 4 != 0:
                mesas += 1

            available_tables = self._check_availability(date, mesas)

            if available_tables is None:
                messages.append("Error al verificar disponibilidad")
                bc.show_errors(messages)
                return

            if available_tables >= mesas:
                self._make_booking(mesas, date)
            else:
                messages.append(
                    f"No hay mesas disponibles para el horario seleccionado. Mesas disponibles: {available_tables} (4 personas por mesa)")
                BasicController.show_errors(messages)

        except ValueError as e:
            messages.append("Error en el formato de los datos")
            bc.show_errors(messages)

