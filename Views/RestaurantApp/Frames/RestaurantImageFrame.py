import os

from tkinter import filedialog
from PIL import Image as PILImage
import customtkinter as ctk
from Controllers import  BasicController

class ImagesFrame(ctk.CTkFrame):
    def __init__(self, parent, db, CIF):
        super().__init__(parent)
        self.db = db
        self.CIF = CIF
        self.images = []
        self.current_index = 0
        self.image_folder = os.path.join(self.db.images_dir, self.CIF)
        self.setup_ui()
        self.load_images()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)

        self.title = ctk.CTkLabel(
            self,
            text="Imágenes del Restaurante",
            font=("Helvetica", 36, "bold")
        )
        self.title.grid(row=0, column=0, pady=(20, 10))

        self.image_navigation_frame = ctk.CTkFrame(self, fg_color="#222222", corner_radius=10)
        self.image_navigation_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.image_navigation_frame.grid_columnconfigure(1, weight=1)

        self.left_button = ctk.CTkButton(
            self.image_navigation_frame,
            text="←",
            command=self.previous_image,
            width=50,
            font=("Helvetica", 18)
        )
        self.left_button.grid(row=0, column=0, padx=(20, 10), pady=10)

        self.image_label = ctk.CTkLabel(self.image_navigation_frame, text="", width=400, height=300)
        self.image_label.grid(row=0, column=1, padx=10, pady=10)

        self.right_button = ctk.CTkButton(
            self.image_navigation_frame,
            text="→",
            command=self.next_image,
            width=50,
            font=("Helvetica", 18)
        )
        self.right_button.grid(row=0, column=2, padx=(10, 20), pady=10)

        self.upload_button = ctk.CTkButton(
            self.image_navigation_frame,
            text="Subir Nueva Imagen",
            command=self.upload_image,
            height=40,
            font=("Helvetica", 16)
        )
        self.upload_button.grid(row=1, column=0, columnspan=3, pady=10)

        self.delete_button = ctk.CTkButton(
            self.image_navigation_frame,
            text="Eliminar Imagen",
            command=self.delete_image,
            height=40,
            font=("Helvetica", 16),
            fg_color="#FF4B4B"
        )
        self.delete_button.grid(row=2, column=0, columnspan=3, pady=10)

    def load_images(self):
        self.images = [image[0] for image in self.db.get_restaurant_images(self.CIF)]
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
                max_width = 400
                max_height = 400
                width, height = pil_image.size

                ratio = min(max_width / width, max_height / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)

                pil_image = pil_image.resize((new_width, new_height), PILImage.Resampling.LANCZOS)
                ctk_image = ctk.CTkImage(pil_image)

                ctk_image = ctk.CTkImage(light_image=pil_image, size=(new_width, new_height))
                self.image_label.configure(image=ctk_image, text="")
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

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar Imagen",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )

        if file_path:
            try:
                new_filename = self.db.add_restaurant_image(self.CIF, file_path)
                if new_filename:
                    self.load_images()
                    BasicController.usage_window("Éxito", "Imagen subida correctamente")
                    self.current_index = len(self.images) - 1
                    self.show_image()
                else:
                    BasicController.show_errors(["Error al subir la imagen."])
            except Exception as e:
                BasicController.show_errors([f"Error al subir la imagen: {str(e)}"])

    def delete_image(self):
        if not self.images:
            BasicController.show_errors(["No hay imágenes para eliminar."])
            return

        filename_to_delete = self.images[self.current_index]
        file_path_to_delete = os.path.join(self.image_folder, filename_to_delete)

        try:
            success = self.db.delete_restaurant_image(self.CIF, filename_to_delete)
            if success:
                if os.path.exists(file_path_to_delete):
                    os.remove(file_path_to_delete)
                self.load_images()
                BasicController.usage_window("Éxito", "Imagen eliminada correctamente")
            else:
                BasicController.show_errors(["Error al eliminar la imagen."])
        except Exception as e:
            BasicController.show_errors([f"Error al eliminar la imagen: {str(e)}"])



