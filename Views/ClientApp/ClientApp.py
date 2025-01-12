import customtkinter as ctk
from Controllers import DataBaseController, BasicController
from Views.ClientApp.Frames.ClientInfoFrame import ClientInfoFrame
from Views.ClientApp.Frames.ClientBookingFrame import ClientBookingsFrame
from Views.ClientApp.Frames.ClientRestaurantsFrame import ClientRestaurantsFrame
from Views.ClientApp.Frames.AddBookingFrame import BookingWindow
from Views.ClientApp.Frames.ClientReviewsFrame import ClientReviewsFrame

SIDEBAR_WIDTH = 200
STANDARD_PAD = 20
TITLE_FONT = ("Helvetica", 22)
SUBTITLE_FONT = ("Helvetica", 30)
NORMAL_FONT = ("Helvetica", 14)
SIDEBAR_BUTTON_HEIGHT = 70

original_client_data = {
    'dni': '',
    'name': '',
    'surname': '',
    'phone': '',
    'username': ''
}

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, width):
        super().__init__(parent, width=width)
        self.setup_ui()

    def setup_ui(self):
        self.grid_rowconfigure(5, weight=1)

        self.title = ctk.CTkLabel(
            self,
            text="Client\nProfile",
            font=TITLE_FONT,
            pady=STANDARD_PAD,
        )
        self.title.grid(row=0, column=0, padx=STANDARD_PAD, pady=STANDARD_PAD)

        buttons = [
            ("info", "Mi Información", 1),
            ("bookings", "Mis Reservas", 2),
            ("restaurants", "Restaurantes", 3),
            ("reviews", "Mis Reseñas", 4)
        ]

        for btn_id, text, row in buttons:
            btn = self.create_sidebar_button(text, None)
            btn.grid(row=row, column=0, padx=0, pady=2, sticky="ew")
            self.set_hover_effect(btn)
            setattr(self, f"btn_{btn_id}", btn)

    def create_sidebar_button(self, text, command):
        return ctk.CTkButton(
            self,
            text=text,
            command=command,
            fg_color="gray",
            text_color="white",
            hover_color=None,
            corner_radius=5,
            height=70,
        )

    def set_hover_effect(self, button):
        default_color = "gray"
        hover_color = "#1E90FF"
        button.bind("<Enter>", lambda e: button.configure(fg_color=hover_color))
        button.bind("<Leave>", lambda e: button.configure(fg_color=default_color))

    def bind_commands(self, info_command, bookings_command, restaurants_command, reviews_command):
        self.btn_info.configure(command=info_command)
        self.btn_bookings.configure(command=bookings_command)
        self.btn_restaurants.configure(command=restaurants_command)
        self.btn_reviews.configure(command=reviews_command)

class MainWindow:
    def __init__(self, root, db, dni):
        self.root = root
        self.db = db
        self.dni = dni
        self.setup_ui()

    def setup_ui(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.sidebar = Sidebar(self.root, width=SIDEBAR_WIDTH)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.content_frame = ctk.CTkFrame(self.root)
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.frames = {
            "info": ClientInfoFrame(self.content_frame, self.db, self.dni),
            "bookings": ClientBookingsFrame(self.content_frame, self.db, self.dni),
            "restaurants": ClientRestaurantsFrame(self.content_frame, self.db, self.dni),
            "reviews": ClientReviewsFrame(self.content_frame, self.db, self.dni)
        }

        self.sidebar.bind_commands(
            info_command=lambda: self.show_frame("info"),
            bookings_command=lambda: self.show_frame("bookings"),
            restaurants_command=lambda: self.show_frame("restaurants"),
            reviews_command=lambda: self.show_frame("reviews")
        )

        self.show_frame("info")

    def show_frame(self, frame_name):

        for frame in self.frames.values():
            if hasattr(frame, 'disable_scroll'):
                frame.disable_scroll()


        for frame in self.frames.values():
            frame.grid_forget()


        if frame_name in self.frames:
            self.frames[frame_name].grid(row=0, column=0, sticky="nsew")
            if hasattr(self.frames[frame_name], "enable_scroll"):
                self.frames[frame_name].enable_scroll()
            if hasattr(self.frames[frame_name], "load_info"):
                self.frames[frame_name].load_info()
            elif hasattr(self.frames[frame_name], "load_bookings"):
                self.frames[frame_name].load_bookings()
            elif hasattr(self.frames[frame_name], "load_filtered_restaurants"):
                self.frames[frame_name].load_filtered_restaurants()
            elif hasattr(self.frames[frame_name], "load_reviews"):
                self.frames[frame_name].load_reviews()

    def open_booking_window(self, restaurant_data):
        BookingWindow(self.root, self.db, restaurant_data, self.dni, bookings_frame=self.frames["bookings"])

def main(db, dni):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    window = ctk.CTk()
    window.title("Client Profile")
    window.geometry("1100x700")
    BasicController.center_window(window, 1100, 700)
    window.iconbitmap(BasicController.obtain_icon_path())
    app = MainWindow(window, db, dni)
    window.mainloop()


if __name__ == "__main__":
    db = DataBaseController()
    dni = "12345678A"
    main(db, dni)
