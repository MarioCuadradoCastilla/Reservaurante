import shutil
import os
import uuid
from tkinter import ttk, filedialog
import customtkinter as ctk
from datetime import datetime
from Controllers import DataBaseController, BasicController
import re

original_restaurant_data = {
    'name': '',
    'address': '',
    'municipality': '',
    'tables': '',
    'phone': '',
    'description': ''
}
class InfoFrame(ctk.CTkFrame):
    def __init__(self, parent, db, CIF):
        super().__init__(parent)
        self.db = db
        self.CIF = CIF
        self.setup_ui()
        self.load_restaurant_data()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._create_title()
        self._create_info_frame()
        self._create_save_button()

    def _create_title(self):
        self.title = ctk.CTkLabel(
            self,
            text="Información del Restaurante",
            font=("Helvetica", 36, "bold")
        )
        self.title.grid(row=0, column=0, padx=120, pady=(50, 10), sticky="n")

    def _create_info_frame(self):
        self.info_frame = ctk.CTkFrame(self, width=600, height=480)
        self.info_frame.grid(row=1, column=0, padx=20, pady=0, sticky="ew")
        self.info_frame.grid_propagate(False)
        self.info_frame.grid_columnconfigure(0, weight=1)

        self.labels = {}
        self.entries = {}
        self.edit_buttons = {}

        fields = [
            ("CIF", "cif", False),
            ("Nombre", "name", True),
            ("Dirección", "address", True),
            ("Municipio", "municipality", "combobox"),
            ("Mesas", "tables", True),
            ("Teléfono", "phone", True)
        ]

        for i, (display_name, field_name, field_type) in enumerate(fields):
            self._create_field_container(i, display_name, field_name, field_type)

        self._create_description_field()

    def _create_field_container(self, row, display_name, field_name, field_type):
        container = ctk.CTkFrame(self.info_frame)
        container.grid(row=row, column=0, padx=10, pady=5, sticky="ew")
        container.grid_columnconfigure(1, weight=1)

        label = ctk.CTkLabel(
            container,
            text=f"{display_name}:",
            font=("Helvetica", 18),
            width=100
        )
        label.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")

        self.labels[field_name] = ctk.CTkLabel(
            container,
            text="",
            font=("Helvetica", 18)
        )
        self.labels[field_name].grid(row=0, column=1, padx=5, pady=5, sticky="w")

        if field_type == "combobox":
            self._setup_municipality_field(container, field_name)
        elif field_type:
            self._setup_editable_field(container, field_name)

        if field_type:
            self._create_edit_button(container, field_name)

    def _setup_municipality_field(self, container, field_name):
        municipalities = BasicController.load_municipalities()
        self.entries[field_name] = ttk.Combobox(
            container,
            values=municipalities,
            width=27,
            font=("Helvetica", 18),
            state="readonly"
        )
        self.entries[field_name].grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.entries[field_name].grid_remove()

    def _setup_editable_field(self, container, field_name):
        self.entries[field_name] = ctk.CTkEntry(
            container,
            font=("Helvetica", 18)
        )
        self.entries[field_name].grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.entries[field_name].grid_remove()

    def _create_edit_button(self, container, field_name):
        edit_btn = ctk.CTkButton(
            container,
            text="Edit",
            width=60,
            command=lambda f=field_name: self.edit_field(f)
        )
        edit_btn.grid(row=0, column=2, padx=5, pady=5)
        self.edit_buttons[field_name] = edit_btn

    def _create_description_field(self):
        description_container = ctk.CTkFrame(self.info_frame)
        description_container.grid(row=6, column=0, padx=10, pady=5, sticky="ew")
        description_container.grid_columnconfigure(0, weight=1)

        description_label = ctk.CTkLabel(
            description_container,
            text="Descripción:",
            font=("Helvetica", 18)
        )
        description_label.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")

        self.description_entry = ctk.CTkTextbox(
            description_container,
            width=580,
            height=100,
            font=("Helvetica", 18)
        )
        self.description_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        self.description_entry.insert("1.0", "")

        self.edit_description_button = ctk.CTkButton(
            description_container,
            text="Editar",
            command=self.edit_description
        )
        self.edit_description_button.grid(row=2, column=0, padx=10, pady=5)

    def _create_save_button(self):
        self.save_button = ctk.CTkButton(
            self,
            text="Guardar",
            font=("Helvetica", 14),
            command=self.guardar_cambios
        )
        self.save_button.grid(row=2, column=0, pady=20)

    def load_restaurant_data(self):
        restaurant = self.db.obtain_restaurant(self.CIF)
        if restaurant:
            global original_restaurant_data
            original_restaurant_data = {
                'name': str(restaurant.name),
                'address': str(restaurant.address),
                'municipality': str(restaurant.municipality),
                'tables': str(restaurant.tables),
                'phone': str(restaurant.phone),
                'description': str(restaurant.description)
            }

            self.labels['cif'].configure(text=str(restaurant.cif))
            for field in ['name', 'address', 'municipality', 'tables', 'phone']:
                self.labels[field].configure(text=str(getattr(restaurant, field)))

            self.description_entry.delete("1.0", "end")
            self.description_entry.insert("1.0", restaurant.description)
            self.description_entry.configure(state="disabled")

    def edit_description(self):
        self.edit_description_button.configure(text="Guardar", command=self.save_description)
        self.description_entry.configure(state="normal")

    def edit_field(self, field_name):
        if field_name == 'cif':
            return

        if self.entries[field_name].winfo_viewable():
            self._save_field(field_name)
        else:
            self._show_field_editor(field_name)

    def _save_field(self, field_name):
        new_value = self.entries[field_name].get()
        validation_errors = self._validate_field(field_name, new_value)

        if validation_errors:
            BasicController.show_errors(validation_errors)
            if field_name != 'municipality':
                self.entries[field_name].configure(border_color="red")
        else:
            if field_name != 'municipality':
                self.entries[field_name].configure(border_color="")
            self.labels[field_name].configure(text=new_value)
            self.labels[field_name].grid()
            self.entries[field_name].grid_remove()
            self.edit_buttons[field_name].configure(text="Edit")

    def _validate_field(self, field_name, value):
        errors = []
        if field_name == 'name':
            if not value.strip():
                errors.append(f"El campo de {field_name} no puede estar vacío.")
            elif self.db.obtain_restaurant_name(value):
                errors.append("El nombre del restaurante ya está registrado, prueba con otro")
        elif field_name == 'address':
            if not value.strip():
                errors.append("La dirección no puede estar vacía.")
        elif field_name == 'municipality':
            municipalities = BasicController.load_municipalities()
            if value not in municipalities:
                errors.append("Selecciona un municipio válido.")
        elif field_name == 'tables':
            if not value.isdigit() or int(value) <= 0:
                errors.append("El número de mesas debe ser un número entero positivo.")
        elif field_name == 'phone':
            if not value.isdigit() or len(value) != 9:
                errors.append("El número de teléfono debe tener 9 números y solo debe contener números.")
        elif field_name == 'password':
            if not (len(value) >= 7 and re.search(r'\d', value) and re.search(r'[A-Z]', value)
                    and re.search(r'[a-z]', value) and re.search(r'[@#$€]', value)):
                errors.append(
                    "La contraseña debe tener al menos 7 caracteres, una letra mayúscula, una letra minúscula, un número y un carácter especial (@#$€).")
        return errors

    def _show_field_editor(self, field_name):
        current_value = self.labels[field_name].cget("text")
        if isinstance(self.entries[field_name], ttk.Combobox):
            self.entries[field_name].set(current_value)
        else:
            self.entries[field_name].delete(0, 'end')
            self.entries[field_name].insert(0, current_value)
        self.labels[field_name].grid_remove()
        self.entries[field_name].grid()
        self.edit_buttons[field_name].configure(text="Save")

    def save_description(self):
        new_description = self.description_entry.get("1.0", "end-1c")
        restaurant = self.db.obtain_restaurant(self.CIF)
        restaurant.description = new_description
        self.db.update_restaurant(restaurant)

        self.description_entry.delete("1.0", "end")
        self.description_entry.insert("1.0", new_description)
        self.edit_description_button.configure(text="Editar", command=self.edit_description)
        self.description_entry.configure(state="disabled")

    def _has_changes(self):
        current_values = {
            'name': self.labels['name'].cget("text"),
            'address': self.labels['address'].cget("text"),
            'municipality': self.labels['municipality'].cget("text"),
            'tables': self.labels['tables'].cget("text"),
            'phone': self.labels['phone'].cget("text"),
            'description': self.description_entry.get("1.0", "end-1c")
        }
        return any(
            current_values[field] != original_restaurant_data[field]
            for field in original_restaurant_data
        )

    def guardar_cambios(self):
        errors = []
        try:
            if not self._has_changes():
                errors.append("No se han realizado cambios")
                BasicController.show_errors(errors)
                return

            restaurant = self.db.obtain_restaurant(self.CIF)
            if not restaurant:
                raise Exception("Restaurant not found")

            restaurant.name = self.labels['name'].cget("text")
            restaurant.address = self.labels['address'].cget("text")
            restaurant.municipality = self.labels['municipality'].cget("text")
            restaurant.tables = int(self.labels['tables'].cget("text"))
            restaurant.phone = int(self.labels['phone'].cget("text"))
            restaurant.description = self.description_entry.get("1.0", "end-1c")

            if self.db.update_restaurant(restaurant):
                global original_restaurant_data
                original_restaurant_data = {
                    'name': restaurant.name,
                    'address': restaurant.address,
                    'municipality': restaurant.municipality,
                    'tables': str(restaurant.tables),
                    'phone': str(restaurant.phone),
                    'description': str(restaurant.description)
                }
                BasicController.usage_window("Éxito", "Cambios guardados correctamente")
            else:
                raise Exception("Failed to update restaurant")

        except Exception as e:
            errors.append(f"Error: No se pudieron guardar los cambios: {str(e)}")
            BasicController.show_errors(errors)