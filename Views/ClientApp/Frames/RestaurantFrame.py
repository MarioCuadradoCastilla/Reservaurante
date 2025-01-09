import customtkinter as ctk
from PIL import Image as PILImage
import os
from datetime import datetime
from Controllers import BasicController
from Views.ClientApp.Frames.AddBookingFrame import BookingWindow
from Views.ClientApp.Frames.AddReviewFrame import  ReviewWindow


class RestaurantFrame(ctk.CTkFrame):
    def __init__(self, parent, db, restaurant_data, dni,username):
        super().__init__(parent)
        self.db = db
        self.restaurant_data = restaurant_data
        self.dni = dni
        self.username = username
        self.images = []
        self.current_index = 0
        self.image_folder = os.path.join(self.db.images_dir, self.restaurant_data['cif'])

    def show_restaurant_details(self, restaurant_data, dni):
        details_window = ctk.CTkToplevel(self)
        details_window.title(restaurant_data['name'])
        BasicController.center_window(details_window, 800, 600)

        details_window.grid_columnconfigure(0, weight=0)
        details_window.grid_columnconfigure(1, weight=1)

        image_navigation_frame = ctk.CTkFrame(details_window, fg_color="#222222", corner_radius=10)
        image_navigation_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        image_navigation_frame.grid_columnconfigure(1, weight=1)

        left_button = ctk.CTkButton(
            image_navigation_frame,
            text="←",
            command=self.previous_image,
            width=50,
            font=("Helvetica", 18)
        )
        left_button.grid(row=0, column=0, padx=(20, 10), pady=10)

        self.image_label = ctk.CTkLabel(image_navigation_frame, text="", width=200, height=200)
        self.image_label.grid(row=0, column=1, padx=10, pady=10)

        right_button = ctk.CTkButton(
            image_navigation_frame,
            text="→",
            command=self.next_image,
            width=50,
            font=("Helvetica", 18)
        )
        right_button.grid(row=0, column=2, padx=(10, 20), pady=10)

        details_frame = ctk.CTkFrame(details_window, fg_color="transparent")
        details_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        title = ctk.CTkLabel(
            details_frame,
            text=restaurant_data['name'],
            font=("Helvetica", 24, "bold")
        )
        title.pack(pady=(0, 10))

        rating = self.db.calculate_restaurant_rating(restaurant_data['cif'])
        rounded_rating = round(rating * 10) / 10
        details = ctk.CTkLabel(
            details_frame,
            text=f"Municipio: {restaurant_data['municipality']}\n\n"
                 f"Dirección: {restaurant_data['address']}\n\n"
                 f"Valoración: {rounded_rating}",
            font=("Helvetica", 16)
        )
        details.pack(pady=10)

        buttons_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)

        reserve_button = ctk.CTkButton(
            buttons_frame,
            text="Reservar",
            command=lambda: self.open_booking_window(restaurant_data)
        )
        reserve_button.pack(side="left", padx=5)

        review_button = ctk.CTkButton(
            buttons_frame,
            text="Hacer Reseña",
            command=lambda: self.open_review_window(restaurant_data)
        )
        review_button.pack(side="left", padx=5)

        reviews_frame = ctk.CTkFrame(details_window)
        reviews_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="nsew")
        reviews_frame.grid_columnconfigure(0, weight=1)
        reviews_frame.grid_rowconfigure(1, weight=1)

        reviews_title = ctk.CTkLabel(
            reviews_frame,
            text="Reseñas",
            font=("Helvetica", 20, "bold")
        )
        reviews_title.grid(row=0, column=0, pady=(10, 5))

        reviews_scrollable_frame = ctk.CTkScrollableFrame(
            reviews_frame,
            fg_color="transparent"
        )
        reviews_scrollable_frame.grid(row=1, column=0, sticky="nsew")
        reviews_scrollable_frame.grid_columnconfigure(0, weight=1)

        self.reviews_scrollable_frame = reviews_scrollable_frame
        self.load_reviews(reviews_scrollable_frame, restaurant_data['cif'])

        details_window.grab_set()
        self.load_images()

    def load_images(self):
        """Carga las imágenes del restaurante desde la base de datos y actualiza la vista."""
        self.images = [image[0] for image in self.db.get_restaurant_images(self.restaurant_data['cif'])]
        self.current_index = 0
        if self.images:
            self.show_image()
        else:
            self.image_label.configure(image=None, text="No hay imágenes disponibles")

    def show_image(self):
        if not self.images:
            return

        filename = self.images[self.current_index]
        file_path = os.path.join(self.image_folder, filename)

        if os.path.exists(file_path):
            try:
                pil_image = PILImage.open(file_path)

                max_width = 200
                max_height = 200

                width, height = pil_image.size

                ratio = min(max_width / width, max_height / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)

                pil_image = pil_image.resize((new_width, new_height), PILImage.Resampling.LANCZOS)

                ctk_image = ctk.CTkImage(pil_image)

                self.image_label.configure(image=ctk_image, text="")
                self.image_label.image = ctk_image

                ctk_image = ctk.CTkImage(light_image=pil_image, size=(new_width, new_height))
                self.image_label.configure(image=ctk_image)
                self.image_label.image = ctk_image
            except Exception as e:
                print(f"Error al mostrar la imagen: {e}")

    def next_image(self):
        if self.images:
            self.current_index = (self.current_index + 1) % len(self.images)
            self.show_image()

    def previous_image(self):
        if self.images:
            self.current_index = (self.current_index - 1) % len(self.images)
            self.show_image()

    def open_booking_window(self, restaurant_data):
        BookingWindow(self, self.db, restaurant_data, self.dni)

    def open_review_window(self, restaurant_data):
        ReviewWindow(self, self.db, restaurant_data, self.dni, self.username)

    def load_reviews(self, reviews_scrollable_frame, cif):
        reviews = self.db.get_restaurant_reviews(cif)

        for i, review in enumerate(reviews):
            self._create_review_frame(reviews_scrollable_frame, i, review)

            if i < len(reviews) - 1:
                separator = ctk.CTkLabel(
                    reviews_scrollable_frame,
                    text="",
                    height=1,
                    fg_color="transparent"
                )
                separator.grid(row=i * 2 + 1, column=0, padx=10, pady=5, sticky="ew")

    def _create_review_frame(self, parent_frame, index, review):
        review_frame = ctk.CTkFrame(
            parent_frame,
            corner_radius=10,
            fg_color="#333333"
        )
        review_frame.grid(row=index * 2, column=0, padx=10, pady=(5, 0), sticky="ew")
        parent_frame.grid_columnconfigure(0, weight=1)

        user_name = review[1]
        rating = review[3]
        rating_int = int(rating)
        rating_str = "★" * rating_int + "☆" * (5 - rating_int)

        review_date = review[5]
        if isinstance(review_date, str):
            try:
                review_date = datetime.strptime(review_date, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                review_date = datetime.now()

        formatted_date = review_date.strftime('%d/%m/%Y')
        review_header = f"Usuario: {user_name},    Valoración: {rating_str} ({rating}),    Fecha: {formatted_date}"

        review_header_label = ctk.CTkLabel(
            review_frame,
            text=review_header,
            font=("Helvetica", 16, "bold"),
            justify="left",
            padx=10,
            pady=10
        )
        review_header_label.pack(fill="x", expand=True)

        comment = review[4]
        comment_textbox = ctk.CTkTextbox(
            review_frame,
            height=60,
            font=("Helvetica", 14),
            state="normal"
        )
        comment_textbox.pack(padx=10, pady=(5, 10), fill="x", expand=True)
        comment_textbox.insert("1.0", comment)
        comment_textbox.configure(state="disabled")