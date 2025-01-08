import customtkinter as ctk
from datetime import datetime
from Models.Review import Review
from Controllers.BasicController import BasicController as bc

class ReviewWindow:
    def __init__(self, parent, db, restaurant_data, dni, username):
        self.parent = parent
        self.window = ctk.CTkToplevel(parent)
        self.window.title(f"Reseña - {restaurant_data['name']}")
        bc.center_window(self.window, 400, 460)
        self.db = db
        self.restaurant_data = restaurant_data
        self.dni = dni
        self.username = username

        self.window.grab_set()
        self._init_ui()


    def _init_ui(self):
        title = ctk.CTkLabel(
            self.window,
            text="Reseña",
            font=("Helvetica", 20, "bold")
        )
        title.pack(pady=20)

        rating_frame = ctk.CTkFrame(self.window)
        rating_frame.pack(fill="x", padx=20, pady=10)

        rating_label = ctk.CTkLabel(rating_frame, text="Valoración (1-5):")
        rating_label.pack(side="left", padx=5)

        self.rating_combobox = ctk.CTkOptionMenu(rating_frame, values=["1", "2", "3", "4", "5"])
        self.rating_combobox.pack(side="right", expand=True, fill="x", padx=5)
        self.rating_combobox.set("1")  # Default value

        comment_label = ctk.CTkLabel(self.window, text="Comentario:")
        comment_label.pack(padx=20, pady=(10, 5), anchor="w")

        self.comment_text = ctk.CTkTextbox(
            self.window,
            height=200
        )
        self.comment_text.pack(padx=20, fill="x")

        submit_btn = ctk.CTkButton(
            self.window,
            text="Publicar Reseña",
            command=self._handle_submit
        )
        submit_btn.pack(pady=20)

    def _handle_submit(self):
        try:
            rating = int(self.rating_combobox.get())
            comment = self.comment_text.get("1.0", "end-1c")

            review = Review(
                clientDNI=self.dni,
                clientUsername=self.username,
                restaurantCIF=self.restaurant_data['cif'],
                rating=rating,
                comment=comment,
                date=datetime.now()
            )

            self.db.add_review(review)

            if hasattr(self.parent, 'load_reviews'):
                self.parent.load_reviews(self.parent.reviews_scrollable_frame, self.restaurant_data['cif'])

            self.window.destroy()

        except ValueError as e:
            error_label = ctk.CTkLabel(
                self.window,
                text="Error en el formato de los datos",
                text_color="red"
            )
            error_label.pack(pady=10)






