
import customtkinter as ctk
from datetime import datetime

class ReviewsFrame(ctk.CTkFrame):
    def __init__(self, parent, db, CIF):
        super().__init__(parent)
        self.db = db
        self.CIF = CIF
        self.setup_ui()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)

        self.title = ctk.CTkLabel(
            self,
            text="Reseñas",
            font=("Helvetica", 30)
        )
        self.title.grid(row=0, column=0, padx=20, pady=20)

        self.reviews_list_frame = ctk.CTkScrollableFrame(self, height=500)
        self.reviews_list_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        self.load_reviews()

    def disable_scroll(self):
        self.reviews_list_frame.unbind_all("<MouseWheel>")
        self.reviews_list_frame.unbind_all("<Button-4>")
        self.reviews_list_frame.unbind_all("<Button-5>")

    def enable_scroll(self):
        self.reviews_list_frame.bind_all("<MouseWheel>", self.reviews_list_frame._mouse_wheel_all)
        self.reviews_list_frame.bind_all("<Button-4>", self.reviews_list_frame._mouse_wheel_all)
        self.reviews_list_frame.bind_all("<Button-5>", self.reviews_list_frame._mouse_wheel_all)

    def load_reviews(self):
        for widget in self.reviews_list_frame.winfo_children():
            widget.destroy()

        reviews = self.db.get_restaurant_reviews(self.CIF)

        for i, review in enumerate(reviews):
            self._create_review_frame(i, review)

        self._create_average_rating_frame()

    def _create_review_frame(self, index, review):
        review_frame = ctk.CTkFrame(
            self.reviews_list_frame,
            corner_radius=10,
            fg_color="#333333"
        )
        review_frame.grid(row=index, column=0, padx=10, pady=(5, 0), sticky="ew")
        self.reviews_list_frame.grid_columnconfigure(0, weight=1)

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

        if index < len(self.db.get_restaurant_reviews(self.CIF)) - 1:
            separator = ctk.CTkLabel(
                self.reviews_list_frame,
                text="",
                height=2,
                fg_color="gray"
            )
            separator.grid(row=index + 1, column=0, padx=10, pady=5, sticky="ew")

    def _create_average_rating_frame(self):
        average_rating = self.db.calculate_restaurant_rating(self.CIF)
        full_stars = int(average_rating)
        half_star = (average_rating - full_stars) >= 0.5
        empty_stars = 5 - full_stars - (1 if half_star else 0)
        stars_str = "★" * full_stars + ("☆" if half_star else "") + "☆" * empty_stars

        average_frame = ctk.CTkFrame(self, fg_color="#333333", corner_radius=10)
        average_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

        average_label = ctk.CTkLabel(
            average_frame,
            text=f"Valoración media: {stars_str} ({average_rating:.1f})",
            font=("Helvetica", 18, "bold"),
            padx=10,
            pady=10
        )
        average_label.pack(fill="x", expand=True)