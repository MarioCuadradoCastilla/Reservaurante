import customtkinter as ctk
from tkinter import ttk
from PIL import Image as PILImage
import os
from Controllers import BasicController
from Views.ClientApp.Frames.RestaurantFrame import RestaurantFrame

class ClientRestaurantsFrame(ctk.CTkFrame):
    def __init__(self, parent, db, dni):
        super().__init__(parent)
        self.db = db
        self.dni = dni
        self.current_municipality = "Todos"
        self.current_sort_option = "nombre"
        self.image_labels = {}
        self.restaurant_image_states = {}

        self.setup_ui()
        self.load_filtered_restaurants()


    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._create_title()
        self._create_search_bar()
        self._create_scrollable_frame()

    def _create_title(self):
        self.title = ctk.CTkLabel(
            self,
            text="Restaurantes",
            font=("Helvetica", 36, "bold")
        )
        self.title.grid(row=0, column=0, padx=120, pady=(0, 10), sticky="n")

    def _create_search_bar(self):
        search_frame = ctk.CTkFrame(self)
        search_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        search_frame.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Buscar restaurante...",
            width=300,
            height=40
        )
        self.search_entry.grid(row=0, column=0, padx=(20, 10), pady=20)

        self.filter_button = ctk.CTkButton(
            search_frame,
            text="Filtros",
            width=100,
            height=40,
            command=self.show_filter_menu
        )
        self.filter_button.grid(row=0, column=1, padx=10, pady=20)

        self.search_var = ctk.StringVar()
        self.search_var.trace('w', self._on_search_change)
        self.search_entry.configure(textvariable=self.search_var)

    def _create_scrollable_frame(self):
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=600, height=500)
        self.scrollable_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

    def show_filter_menu(self):
        self.disable_scroll()
        filter_window = ctk.CTkToplevel(self)
        filter_window.title("Filtros")
        filter_window.geometry("300x400")
        BasicController.center_window(filter_window, 300, 400)
        self._setup_filter_window(filter_window)
        filter_window.grab_set()
        filter_window.protocol("WM_DELETE_WINDOW", lambda: self.close_filter_window(filter_window))

    def close_filter_window(self, window):
        self.enable_scroll()
        window.destroy()

    def disable_scroll(self):
        self.scrollable_frame.unbind_all("<MouseWheel>")
        self.scrollable_frame.unbind_all("<Button-4>")
        self.scrollable_frame.unbind_all("<Button-5>")

    def enable_scroll(self):
        self.scrollable_frame.bind_all("<MouseWheel>", self.scrollable_frame._mouse_wheel_all)
        self.scrollable_frame.bind_all("<Button-4>", self.scrollable_frame._mouse_wheel_all)
        self.scrollable_frame.bind_all("<Button-5>", self.scrollable_frame._mouse_wheel_all)

    def _setup_filter_window(self, window):
        sort_label = ctk.CTkLabel(window, text="Ordenar por:")
        sort_label.pack(pady=10)

        self.sort_var = ctk.StringVar(value="nombre")
        sort_options = ["Nombre", "Valoración", "Municipio"]

        for option in sort_options:
            rb = ctk.CTkRadioButton(
                window,
                text=option,
                variable=self.sort_var,
                value=option.lower()
            )
            rb.pack(pady=5)

        municipality_label = ctk.CTkLabel(window, text="Municipio:")
        municipality_label.pack(pady=10)

        municipalities = BasicController.load_municipalities()
        self.municipality_var = ctk.StringVar(value=self.current_municipality)
        self.municipality_combobox = ttk.Combobox(
            window,
            values=["Todos"] + municipalities,
            height=5,
            font=("Helvetica", 12),
            state="readonly",
            textvariable=self.municipality_var
        )
        self.municipality_combobox.pack(pady=5)

        apply_button = ctk.CTkButton(
            window,
            text="Aplicar",
            command=lambda: self._apply_filters(window)
        )
        apply_button.pack(pady=20)

    def _apply_filters(self, window):
        self.current_municipality = self.municipality_var.get()
        self.current_sort_option = self.sort_var.get()
        self.load_filtered_restaurants()
        self.scrollable_frame._parent_canvas.yview_moveto(0)  # Mueve la barra de desplazamiento al inicio
        self.enable_scroll()
        window.destroy()

    def _create_restaurant_card(self, restaurant_data, row):
        card = ctk.CTkFrame(
            self.scrollable_frame,
            corner_radius=10,
            fg_color="black"
        )
        card.grid(row=row, column=0, sticky="ew", padx=10, pady=5)
        card.grid_columnconfigure(1, weight=1)

        card.bind("<Enter>", lambda e: self._on_card_hover_enter(card))
        card.bind("<Leave>", lambda e: self._on_card_hover_leave(card))
        card.bind("<Button-1>", lambda e: self._on_restaurant_click(restaurant_data))

        cif = restaurant_data['cif']

        image_frame = ctk.CTkFrame(card, fg_color="#222222", corner_radius=10)
        image_frame.grid(row=0, column=0, rowspan=4, padx=10, pady=10, sticky="w")

        image_label = ctk.CTkLabel(image_frame, text="", width=150, height=150)
        image_label.grid(row=0, column=0, padx=10, pady=10)
        self.image_labels[cif] = image_label

        if cif not in self.restaurant_image_states:
            self.restaurant_image_states[cif] = {
                'current_index': 0,
                'images': [],
                'timer_id': None
            }

        self.load_images(cif)

        name_label = ctk.CTkLabel(
            card,
            text=restaurant_data['name'],
            font=("Helvetica", 18, "bold"),
            text_color="white"
        )
        name_label.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        municipality_label = ctk.CTkLabel(
            card,
            text=f"Municipio: {restaurant_data['municipality']}",
            text_color="light gray",
            font=("Helvetica", 16)
        )
        municipality_label.grid(row=1, column=1, sticky="w", padx=10, pady=2)

        address_label = ctk.CTkLabel(
            card,
            text=f"Dirección: {restaurant_data['address']}",
            text_color="light gray",
            font=("Helvetica", 16)
        )
        address_label.grid(row=2, column=1, sticky="w", padx=10, pady=2)

        rating = self.db.calculate_restaurant_rating(restaurant_data['cif'])
        rounded_rating = round(rating * 10) / 10
        rating_label = ctk.CTkLabel(
            card,
            text=f"Valoración: {rounded_rating}",
            text_color="light gray",
            font=("Helvetica", 16)
        )
        rating_label.grid(row=3, column=1, sticky="w", padx=10, pady=5)

    def load_images(self, cif):
        if cif in self.restaurant_image_states and self.restaurant_image_states[cif]['timer_id']:
            self.after_cancel(self.restaurant_image_states[cif]['timer_id'])

        images = [image[0] for image in self.db.get_restaurant_images(cif)]

        self.restaurant_image_states[cif] = {
            'current_index': 0,
            'images': images,
            'timer_id': None
        }

        if images:
            self.show_image(cif)
        else:
            if cif in self.image_labels:
                self.image_labels[cif].configure(image=None, text="No hay imágenes disponibles")

    def show_image(self, cif):
        if cif not in self.restaurant_image_states:
            return

        state = self.restaurant_image_states[cif]
        images = state['images']

        if not images:
            return

        current_index = state['current_index']
        filename = images[current_index]
        image_folder = os.path.join(self.db.images_dir, cif)
        file_path = os.path.join(image_folder, filename)

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
                ctk_image = ctk.CTkImage(light_image=pil_image, size=(new_width, new_height))

                if cif in self.image_labels:
                    image_label = self.image_labels[cif]
                    image_label.configure(image=ctk_image, text="")
                    image_label.image = ctk_image

                timer_id = self.after(5000, lambda: self.next_image(cif))
                self.restaurant_image_states[cif]['timer_id'] = timer_id

            except Exception as e:
                print(f"Error al mostrar la imagen: {e}")
        else:
            print(f"Archivo no encontrado: {file_path}")

    def next_image(self, cif):
        if cif not in self.restaurant_image_states:
            return

        state = self.restaurant_image_states[cif]
        images = state['images']

        if not images:
            return

        state['current_index'] = (state['current_index'] + 1) % len(images)
        self.show_image(cif)

    def _on_card_hover_enter(self, card):
        card.configure(fg_color="#333333")

    def _on_card_hover_leave(self, card):
        card.configure(fg_color="black")

    def _on_restaurant_click(self, restaurant_data):
        username = self.db.get_user_name(self.dni)
        restaurant_frame = RestaurantFrame(self, self.db, restaurant_data, self.dni,username)
        restaurant_frame.show_restaurant_details(restaurant_data)

    def _on_search_change(self, *args):
        self.filter_restaurants(self.search_entry.get())

    def load_filtered_restaurants(self):
        for cif in self.restaurant_image_states:
            if self.restaurant_image_states[cif]['timer_id']:
                self.after_cancel(self.restaurant_image_states[cif]['timer_id'])
                self.restaurant_image_states[cif]['timer_id'] = None

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if self.current_municipality == "Todos":
            query = "SELECT * FROM Restaurant"
            params = ()
        else:
            query = "SELECT * FROM Restaurant WHERE municipality = ?"
            params = (self.current_municipality,)

        self.db.cursor.execute(query, params)
        restaurants = self.db.cursor.fetchall()

        restaurant_list = []
        for restaurant in restaurants:
            restaurant_data = {
                'cif': restaurant[0],
                'address': restaurant[1],
                'name': restaurant[2],
                'municipality': restaurant[4],
                'rating': self.db.calculate_restaurant_rating(restaurant[0])
            }
            restaurant_list.append(restaurant_data)

        if self.current_sort_option == "valoración":
            restaurant_list.sort(key=lambda x: x['rating'], reverse=True)
        elif self.current_sort_option == "nombre":
            restaurant_list.sort(key=lambda x: x['name'].lower())
        elif self.current_sort_option == "municipio":
            restaurant_list.sort(key=lambda x: x['municipality'].lower())

        for i, restaurant_data in enumerate(restaurant_list):
            self._create_restaurant_card(restaurant_data, i)

    def filter_restaurants(self, search_text):

        for cif in self.restaurant_image_states:
            if self.restaurant_image_states[cif]['timer_id']:
                self.after_cancel(self.restaurant_image_states[cif]['timer_id'])
                self.restaurant_image_states[cif]['timer_id'] = None

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if self.current_municipality == "Todos":
            self.db.cursor.execute("""
                SELECT * FROM Restaurant 
                WHERE name LIKE ? OR municipality LIKE ?
            """, (f"%{search_text}%", f"%{search_text}%"))
        else:
            self.db.cursor.execute("""
                SELECT * FROM Restaurant 
                WHERE municipality = ? AND (name LIKE ? OR municipality LIKE ?)
            """, (self.current_municipality, f"%{search_text}%", f"%{search_text}%"))

        restaurants = self.db.cursor.fetchall()

        for i, restaurant in enumerate(restaurants):
            restaurant_data = {
                'cif': restaurant[0],
                'address': restaurant[1],
                'name': restaurant[2],
                'municipality': restaurant[4],
            }
            self._create_restaurant_card(restaurant_data, i)
        self.scrollable_frame._parent_canvas.yview_moveto(0)
