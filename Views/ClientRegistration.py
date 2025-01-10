import re
from Models import Client
import customtkinter as ctk
from Controllers import BasicController
import os



def open_client_registration_window(db, event=None):
    window = ctk.CTk()
    window.title("Registro de Cliente")
    BasicController.center_window(window, 600, 400)
    window.resizable(False, False)

    script_dir = os.path.dirname(os.path.abspath(__file__))

    icon_path = os.path.join(script_dir, "..", "img", "icono.ico")
    if os.path.exists(icon_path):
        window.iconbitmap(icon_path)
    else:
        print(f"Error: El archivo {icon_path} no se encontró.")

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    main_frame = ctk.CTkFrame(window, corner_radius=10)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True, side="left")

    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)

    title_label = ctk.CTkLabel(main_frame, text="Registro de Cliente", font=("Helvetica", 30), anchor='center')
    title_label.grid(row=0, column=0, columnspan=2, pady=10)

    dni_label = ctk.CTkLabel(main_frame, text="DNI:", font=("Helvetica", 18))
    dni_label.grid(row=1, column=0, pady=5, sticky="e")
    dni_entry = ctk.CTkEntry(main_frame, width=300, font=("Helvetica", 12))
    dni_entry.grid(row=1, column=1, pady=5)

    name_label = ctk.CTkLabel(main_frame, text="Nombre:", font=("Helvetica", 18))
    name_label.grid(row=2, column=0, pady=5, sticky="e")
    name_entry = ctk.CTkEntry(main_frame, width=300, font=("Helvetica", 12))
    name_entry.grid(row=2, column=1, pady=5)

    surname_label = ctk.CTkLabel(main_frame, text="Primer Apellido:", font=("Helvetica", 18))
    surname_label.grid(row=3, column=0, pady=5, sticky="e")
    surname_entry = ctk.CTkEntry(main_frame, width=300, font=("Helvetica", 12))
    surname_entry.grid(row=3, column=1, pady=5)

    phone_label = ctk.CTkLabel(main_frame, text="Teléfono:", font=("Helvetica", 18))
    phone_label.grid(row=4, column=0, pady=5, sticky="e")
    phone_entry = ctk.CTkEntry(main_frame, width=300, font=("Helvetica", 12))
    phone_entry.grid(row=4, column=1, pady=5)

    username_label = ctk.CTkLabel(main_frame, text="Nombre de usuario:", font=("Helvetica", 18))
    username_label.grid(row=5, column=0, pady=5, sticky="e")
    username_entry = ctk.CTkEntry(main_frame, width=300, font=("Helvetica", 12))
    username_entry.grid(row=5, column=1, pady=5)

    password_label = ctk.CTkLabel(main_frame, text="Contraseña:", font=("Helvetica", 18))
    password_label.grid(row=6, column=0, pady=5, sticky="e")
    password_entry = ctk.CTkEntry(main_frame, width=300, font=("Helvetica", 12), show='*')
    password_entry.grid(row=6, column=1, pady=5)

    def create_client():
        dni = dni_entry.get()
        name = name_entry.get()
        surname = surname_entry.get()
        phone = phone_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        new_client = Client(dni, name, surname, phone, password, username)
        print(f"Cliente creado: {new_client.name}, {new_client.dni}, {new_client.surname}, {new_client.phone}, {new_client.username}")
        return new_client

    def validation():
        errors = []
        dni = dni_entry.get()
        name = name_entry.get()
        surname = surname_entry.get()
        phone = phone_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        resultado = True

        if not re.match(r"^\d{8}[A-Z]$", dni):
            errors.append("El DNI debe tener 8 números seguidos de una letra mayúscula.")
            dni_entry.configure(border_color="red")
            resultado = False
        else:
            dni_entry.configure(border_color="")

        if not name.strip():
            errors.append("El campo de nombre no puede estar vacío.")
            name_entry.configure(border_color="red")
            resultado = False
        else:
            name_entry.configure(border_color="")

        if not surname.strip():
            errors.append("El campo de primer apellido no puede estar vacío.")
            surname_entry.configure(border_color="red")
            resultado = False
        else:
            surname_entry.configure(border_color="")

        if not phone.isdigit() or len(phone) != 9:
            errors.append("El número de teléfono debe tener 9 números y solo debe contener números.")
            phone_entry.configure(border_color="red")
            resultado = False
        else:
            phone_entry.configure(border_color="")

        if not username.strip():
            errors.append("El campo de nombre de usuario no puede estar vacío.")
            username_entry.configure(border_color="red")
            resultado = False
        else:
            if db.obtain_client_username(username):
                errors.append("El nombre de usuario ya esta registrado, prueba con otro")
                username_entry.configure(border_color="red")
                resultado = False
            else:
                username_entry.configure(border_color="")

        if not (len(password) >= 7 and re.search(r'\d', password) and re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) and re.search(r'[@#$€]', password)):
            errors.append(
                "La contraseña debe tener al menos 7 caracteres, una letra mayúscula, una letra minúscula, un número y un carácter especial (@#$€).")
            password_entry.configure(border_color="red")
            resultado = False
        else:
            password_entry.configure(border_color="")

        if resultado:
            if db.obtain_dni(dni):
                errors.append("El DNI ya está registrado.")
                dni_entry.configure(border_color="red")
                BasicController.show_errors(errors)
            else:
                db.add_client(create_client())
                BasicController.usage_window("Registro exitoso","Registro Completado")
                entries = [dni_entry, name_entry, surname_entry, phone_entry, username_entry, password_entry]

                # Vaciar todas las entradas usando un bucle
                for entry in entries:
                    entry.delete(0, "end")
                    entry.insert(0, "")

        else:
            BasicController.show_errors(errors)



    register_button = ctk.CTkButton(main_frame, text="Registrarse", command=validation)
    register_button.grid(row=7, column=0, columnspan=2, pady=15)
    register_button.bind("<Enter>", lambda event: register_button.configure(cursor="hand2"))
    register_button.bind("<Leave>", lambda event: register_button.configure(cursor=""))

    def add_focus_effect_to_all_entries(container):
        for widget in container.winfo_children():
            if isinstance(widget, ctk.CTkEntry):
                widget.bind("<FocusIn>", lambda event, w=widget: w.configure(border_color="#1E90FF"))
                widget.bind("<FocusOut>", lambda event, w=widget: w.configure(border_color=""))
            elif widget.winfo_children():
                add_focus_effect_to_all_entries(widget)

    add_focus_effect_to_all_entries(main_frame)
    window.protocol("WM_DELETE_WINDOW", lambda: open_Login_on_delete(window, db))
    window.attributes("-topmost", True)

    window.mainloop()


def open_Login_on_delete(current_window, db):
    from Views.ClientLogin import  open_client_login_window
    current_window.destroy()
    open_client_login_window(db)

if __name__ == "__main__":
    from Controllers import DataBaseController

    db = DataBaseController()
    db.open_connection()
    try:
        open_client_registration_window(db)
    finally:
        db.close_connection()