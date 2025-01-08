import customtkinter as ctk
from datetime import datetime

class ClientReviewsFrame(ctk.CTkFrame):
    def __init__(self, parent, db, dni):
        super().__init__(parent)
        self.db = db
        self.dni = dni
        self.setup_ui()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)

        self.title = ctk.CTkLabel(
            self,
            text="Mis Reseñas",
            font=("Helvetica", 30, "bold")
        )
        self.title.grid(row=0, column=0, padx=20, pady=20)

        self.reviews_list_frame = ctk.CTkScrollableFrame(self, height=500)
        self.reviews_list_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        self.load_reviews()

    def load_reviews(self):
        for widget in self.reviews_list_frame.winfo_children():
            widget.destroy()

        reviews = self.db.get_client_reviews(self.dni)

        for i, review in enumerate(reviews):
            self._create_review_frame(i, review)

    def _create_review_frame(self, index, review):
        review_frame = ctk.CTkFrame(
            self.reviews_list_frame,
            corner_radius=10,
            fg_color="#333333"
        )
        review_frame.grid(row=index * 2, column=0, padx=10, pady=(5, 0), sticky="ew")
        self.reviews_list_frame.grid_columnconfigure(0, weight=1)

        rating = review[4]
        rating_int = int(rating)
        rating_str = "★" * rating_int + "☆" * (5 - rating_int)
        review_date = review[6]

        if isinstance(review_date, str):
            try:
                review_date = datetime.strptime(review_date, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                review_date = datetime.now()

        formatted_date = review_date.strftime('%d/%m/%Y')
        review_header = f"Restaurante: {review[7]},   Valoración: {rating_str} ({rating}),    Fecha: {formatted_date}"

        review_header_label = ctk.CTkLabel(
            review_frame,
            text=review_header,
            font=("Helvetica", 16, "bold"),
            justify="left",
            padx=10,
            pady=10
        )
        review_header_label.pack(fill="x", expand=True)

        comment = review[5]
        comment_textbox = ctk.CTkTextbox(
            review_frame,
            height=60,
            font=("Helvetica", 14),
            state="normal"
        )
        comment_textbox.pack(padx=10, pady=(5, 10), fill="x", expand=True)
        comment_textbox.insert("1.0", comment)
        comment_textbox.configure(state="disabled")

        delete_button = ctk.CTkButton(
            review_frame,
            text="Eliminar",
            command=lambda review_id=review[0]: self.delete_review(review_id)
        )
        delete_button.pack(padx=10, pady=(10, 10), fill="x", expand=True)

    def delete_review(self, review_id):
        print(f"Intentando eliminar reseña {review_id}")
        if self.db.delete_review(review_id):
            print("Reseña eliminada exitosamente")
            self.load_reviews()
        else:
            print("Error al eliminar la reseña")


