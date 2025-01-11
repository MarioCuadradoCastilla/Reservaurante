
import customtkinter as ctk
from Controllers import DataBaseController, BasicController
from Views.RestaurantApp.Frames.RestaurnatReviewsFrame import ReviewsFrame
from Views.RestaurantApp.Frames.RestaurantBookingsFrame import BookingsFrame
from Views.RestaurantApp.Frames.RestaurantImageFrame import ImagesFrame
from Views.RestaurantApp.Frames.RestauranInfoFrame import InfoFrame

original_restaurant_data = {
    'name': '',
    'address': '',
    'municipality': '',
    'tables': '',
    'phone': '',
    'description': ''
}


class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, width):
        super().__init__(parent, width=width)
        self.setup_ui()

    def setup_ui(self):
        self.grid_rowconfigure(5, weight=1)

        self.title = ctk.CTkLabel(
            self,
            text="Restaurant\nManager",
            font=("Helvetica", 22),
            pady=20,
        )
        self.title.grid(row=0, column=0, padx=20, pady=20)

        buttons = [
            ("Información del Restaurante", 1),
            ("Reservas", 2),
            ("Reseñas", 3),
            ("Imágenes", 4)
        ]

        for text, row in buttons:
            btn = self.create_sidebar_button(text, None)
            btn.grid(row=row, column=0, padx=0, pady=2, sticky="ew")
            self.set_hover_effect(btn)
            setattr(self, f"btn_{text.lower().split()[0]}", btn)

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

    def bind_commands(self, restaurant_command, bookings_command, reviews_command, images_command):
        self.btn_información.configure(command=restaurant_command)
        self.btn_reservas.configure(command=bookings_command)
        self.btn_reseñas.configure(command=reviews_command)
        self.btn_imágenes.configure(command=images_command)

class MainWindow:
    def __init__(self, root, db, CIF):
        self.root = root
        self.db = db
        self.CIF = CIF
        self.setup_ui()

    def setup_ui(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.sidebar = Sidebar(self.root, width=200)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.content_frame = ctk.CTkFrame(self.root)
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.frames = {
            "restaurant": InfoFrame(self.content_frame, self.db, self.CIF),
            "bookings": BookingsFrame(self.content_frame, self.db, self.CIF),
            "reviews": ReviewsFrame(self.content_frame, self.db, self.CIF),
            "images": ImagesFrame(self.content_frame, self.db, self.CIF)
        }

        self.sidebar.bind_commands(
            restaurant_command=lambda: self.show_frame("restaurant"),
            bookings_command=lambda: self.show_frame("bookings"),
            reviews_command=lambda: self.show_frame("reviews"),
            images_command=lambda: self.show_frame("images")
        )

        self.show_frame("restaurant")

    def show_frame(self, frame_name):
        # Deshabilitar el desplazamiento en todos los frames primero
        for frame in self.frames.values():
            if hasattr(frame, 'disable_scroll'):
                frame.disable_scroll()

        for frame in self.frames.values():
            frame.grid_forget()
            if hasattr(self.frames[frame_name], "enable_scroll"):
                self.frames[frame_name].enable_scroll()
        self.frames[frame_name].grid(row=0, column=0, sticky="nsew")


def main(db, cif):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    window = ctk.CTk()
    window.title("Restaurant Management System")
    window.geometry("1100x700")
    BasicController.center_window(window, 1100, 700)
    window.iconbitmap(BasicController.obtain_icon_path())

    MainWindow(window, db, cif)
    window.mainloop()


if __name__ == "__main__":
    db = DataBaseController()
    cif = "B12345678"
    main(db, cif)