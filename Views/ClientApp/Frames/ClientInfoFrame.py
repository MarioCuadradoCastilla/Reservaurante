import re
import customtkinter as ctk
from Controllers import BasicController

class ClientInfoFrame(ctk.CTkFrame):
    def __init__(self, parent, db, dni):
        super().__init__(parent)
        self.db = db
        self.dni = dni
        self.setup_ui()
        self.load_client_data()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._create_title()
        self._create_info_frame()
        self._create_save_button()

    def _create_title(self):
        self.title = ctk.CTkLabel(
            self,
            text="Mi Información Personal",
            font=("Helvetica", 36, "bold")
        )
        self.title.grid(row=0, column=0, padx=120, pady=(50, 10), sticky="n")

    def _create_info_frame(self):
        self.info_frame = ctk.CTkFrame(self, width=600, height=300)
        self.info_frame.grid(row=1, column=0, padx=20, pady=0, sticky="ew")
        self.info_frame.grid_propagate(False)
        self.info_frame.grid_columnconfigure(0, weight=1)

        self.labels = {}
        self.entries = {}
        self.edit_buttons = {}

        fields = [
            ("DNI", "dni", False),
            ("Nombre", "name", True),
            ("Apellidos", "surname", True),
            ("Teléfono", "phone", True),
            ("Usuario", "username", True),
            ("Contraseña", "password", True)
        ]

        for i, (display_name, field_name, editable) in enumerate(fields):
            self._create_field_container(i, display_name, field_name, editable)

    def _create_field_container(self, row, display_name, field_name, editable):
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

        if editable:
            self._setup_editable_field(container, field_name)
            self._create_edit_button(container, field_name)

    def _setup_editable_field(self, container, field_name):
        self.entries[field_name] = ctk.CTkEntry(
            container,
            font=("Helvetica", 18)
        )
        self.entries[field_name].grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.entries[field_name].grid_remove()

    def _validate_field(self, field_name, value):
        errors = []
        if field_name == 'name' or field_name == 'surname':
            if not value.strip():
                errors.append(f"El campo de {field_name} no puede estar vacío.")
        elif field_name == 'phone':
            if not value.isdigit() or len(value) != 9:
                errors.append("El número de teléfono debe tener 9 números y solo debe contener números.")
        elif field_name == 'username':
            if not value.strip():
                errors.append("El campo de nombre de usuario no puede estar vacío.")
            elif self.db.obtain_client_username(value) and value != original_client_data['username']:
                errors.append("El nombre de usuario ya está registrado, prueba con otro")
        elif field_name == 'password':
            if not (len(value) >= 7 and re.search(r'\d', value) and re.search(r'[A-Z]', value)
                    and re.search(r'[a-z]', value) and re.search(r'[@#$€]', value)):
                errors.append(
                    "La contraseña debe tener al menos 7 caracteres, una letra mayúscula, una letra minúscula, un número y un carácter especial (@#$€).")
        return errors

    def _create_edit_button(self, container, field_name):
        edit_btn = ctk.CTkButton(
            container,
            text="Edit",
            width=60,
            command=lambda f=field_name: self.edit_field(f)
        )
        edit_btn.grid(row=0, column=2, padx=5, pady=5)
        self.edit_buttons[field_name] = edit_btn

    def _create_save_button(self):
        self.save_button = ctk.CTkButton(
            self,
            text="Guardar",
            font=("Helvetica", 14),
            command=self.guardar_cambios
        )
        self.save_button.grid(row=2, column=0, pady=20)

    def load_client_data(self):
        client = self.db.obtain_client(self.dni)
        if client:
            global original_client_data
            original_client_data = {
                'dni': str(client.dni),
                'name': str(client.name),
                'surname': str(client.surname),
                'phone': str(client.phone),
                'username': str(client.username),
                'password': str(client.password)
            }

            for field in ['dni', 'name', 'surname', 'phone', 'username','password']:
                self.labels[field].configure(text=str(getattr(client, field)))

    def edit_field(self, field_name):
        if field_name == 'dni':
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
            self.entries[field_name].configure(border_color="red")
        else:
            self.entries[field_name].configure(border_color="")
            self.labels[field_name].configure(text=new_value)
            self.labels[field_name].grid()
            self.entries[field_name].grid_remove()
            self.edit_buttons[field_name].configure(text="Edit")

    def _show_field_editor(self, field_name):
        current_value = self.labels[field_name].cget("text")
        self.entries[field_name].delete(0, 'end')
        self.entries[field_name].insert(0, current_value)
        self.labels[field_name].grid_remove()
        self.entries[field_name].grid()
        self.edit_buttons[field_name].configure(text="Save")

    def _has_changes(self):
        current_values = {
            'name': self.labels['name'].cget("text"),
            'surname': self.labels['surname'].cget("text"),
            'phone': self.labels['phone'].cget("text"),
            'username': self.labels['username'].cget("text"),
            'password': self.labels['password'].cget("text")
        }
        return any(
            current_values[field] != original_client_data[field]
            for field in current_values
        )

    def guardar_cambios(self):
        errors = []
        try:
            if not self._has_changes():
                errors.append("No se han realizado cambios")
                BasicController.show_errors(errors)
                return

            client = self.db.obtain_client(self.dni)
            if not client:
                raise Exception("Client not found")

            client.name = self.labels['name'].cget("text")
            client.surname = self.labels['surname'].cget("text")
            client.phone = int(self.labels['phone'].cget("text"))
            client.username = self.labels['username'].cget("text")
            client.username = self.labels['password'].cget("text")

            if self.db.update_client(client):
                global original_client_data
                original_client_data = {
                    'dni': client.dni,
                    'name': client.name,
                    'surname': client.surname,
                    'phone': str(client.phone),
                    'username': client.username,
                    'password': client.password
                }
                BasicController.usage_window("Éxito", "Cambios guardados correctamente")
            else:
                raise Exception("Failed to update client")

        except Exception as e:
            errors.append(f"Error: No se pudieron guardar los cambios: {str(e)}")
            BasicController.show_errors(errors)