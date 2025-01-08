import customtkinter as ctk
from datetime import datetime

class BookingsFrame(ctk.CTkFrame):
    def __init__(self, parent, db, CIF):
        super().__init__(parent)
        self.db = db
        self.CIF = CIF
        self.setup_ui()
        self.load_bookings()

        self.grid_columnconfigure((0, 2), weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure((0, 2), weight=1)
        self.grid_rowconfigure(1, weight=0)

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)

        self.title = ctk.CTkLabel(
            self,
            text="Reservas",
            font=("Helvetica", 36, "bold")
        )
        self.title.place(relx=0.5, rely=0.13, anchor="center")

        self.bookings_frame = ctk.CTkScrollableFrame(self, width=240, height=460)
        self.bookings_frame.place(relx=0.5, rely=0.55, anchor='center')

    def load_bookings(self):
        for widget in self.bookings_frame.winfo_children():
            widget.destroy()

        bookings = self.db.get_restaurant_bookings(self.CIF)
        current_time = datetime.now()

        for i, booking in enumerate(bookings):
            self._create_booking_frame(i, booking, current_time)

    def _create_booking_frame(self, index, booking, current_time):
        booking_id = booking[3]
        client_name = self.db.get_user_name(booking[0])
        date_str = booking[1].split('.')[0]
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

        time_diff = current_time - date_obj
        frame_color = "#333333"
        textbox_color = "#55AA55" if time_diff.total_seconds() > 2 * 3600 else "#1C1C1C"

        booking_frame = ctk.CTkFrame(
            self.bookings_frame,
            fg_color=frame_color,
            corner_radius=15
        )
        booking_frame.grid(row=index, column=0, padx=10, pady=(5, 0), sticky="ew")
        self.bookings_frame.grid_columnconfigure(0, weight=1)

        booking_id_label = ctk.CTkLabel(
            booking_frame,
            text=f"ID Reserva: {booking_id}",
            font=("Helvetica", 16, "bold"),
            justify="left",
            padx=10,
            pady=5
        )
        booking_id_label.pack(fill="x")

        formatted_date = date_obj.strftime('%d/%m/%Y %H:%M')
        details = f"Cliente: {client_name}\nFecha: {formatted_date}\nMesas: {booking[2]}"

        booking_textbox = ctk.CTkTextbox(
            booking_frame,
            height=100,
            font=("Helvetica", 14),
            state="normal",
            fg_color=textbox_color
        )
        booking_textbox.pack(padx=10, pady=5, fill="x", expand=True)
        booking_textbox.insert("1.0", details)
        booking_textbox.configure(state="disabled")

        if index < len(self.db.get_restaurant_bookings(self.CIF)) - 1:
            separator = ctk.CTkLabel(
                self.bookings_frame,
                text="",
                height=2,
                fg_color="gray"
            )
            separator.grid(row=index + 1, column=0, padx=10, pady=5, sticky="ew")