from tkinter import ttk
import re
from Models import Restaurant
import customtkinter as ctk
from Controllers import BasicController



def open_restaurant_registration_window(db, event=None):

    window = ctk.CTk()
    window.title("Registro de Restaurante")
    window.resizable(False, False)

    window.iconbitmap(BasicController.obtain_icon_path())

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    BasicController.center_window(window, 600, 420)

    # Frame principal
    main_frame = ctk.CTkFrame(window, corner_radius=10)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True, side="left")

    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)

    title_label = ctk.CTkLabel(main_frame, text="Registro de Restaurante", font=("Helvetica", 30), anchor='center')
    title_label.grid(row=0, column=0, columnspan=2, pady=10)

    cif_label = ctk.CTkLabel(main_frame, text="CIF:", font=("Helvetica", 18))
    cif_label.grid(row=1, column=0, pady=5, sticky="e")
    cif_entry = ctk.CTkEntry(main_frame, width=300, font=("Helvetica", 12))
    cif_entry.grid(row=1, column=1, pady=5)

    address_label = ctk.CTkLabel(main_frame, text="Dirección:", font=("Helvetica", 18))
    address_label.grid(row=2, column=0, pady=5, sticky="e")
    address_entry = ctk.CTkEntry(main_frame, width=300, font=("Helvetica", 12))
    address_entry.grid(row=2, column=1, pady=5)

    name_label = ctk.CTkLabel(main_frame, text="Nombre:", font=("Helvetica", 18))
    name_label.grid(row=3, column=0, pady=5, sticky="e")
    name_entry = ctk.CTkEntry(main_frame, width=300, font=("Helvetica", 12))
    name_entry.grid(row=3, column=1, pady=5)

    phone_label = ctk.CTkLabel(main_frame, text="Teléfono:", font=("Helvetica", 18))
    phone_label.grid(row=4, column=0, pady=5, sticky="e")
    phone_entry = ctk.CTkEntry(main_frame, width=300, font=("Helvetica", 12))
    phone_entry.grid(row=4, column=1, pady=6)

    municipality_label = ctk.CTkLabel(main_frame, text="Municipio:", font=("Helvetica", 18))
    municipality_label.grid(row=5, column=0, pady=5, sticky="e")

    municipios = BasicController.load_municipalities()
    municipality_combobox = ttk.Combobox(main_frame,
                                         values=municipios,
                                         width=27,
                                         font=("Helvetica", 12),
                                         style="TCombobox",
                                         state="readonly")

    municipality_combobox.grid(row=5, column=1, pady=5)
    municipality_combobox.configure(height=5)

    tables_label = ctk.CTkLabel(main_frame, text="Número de mesas:", font=("Helvetica", 18))
    tables_label.grid(row=6, column=0, pady=5, sticky="e")
    tables_entry = ctk.CTkEntry(main_frame, width=300, font=("Helvetica", 12))
    tables_entry.grid(row=6, column=1, pady=5)

    password_label = ctk.CTkLabel(main_frame, text="Contraseña:", font=("Helvetica", 18))
    password_label.grid(row=7, column=0, pady=5, sticky="e")
    password_entry = ctk.CTkEntry(main_frame, width=300, font=("Helvetica", 12),show='*')
    password_entry.grid(row=7, column=1, pady=5)

    def create_restaurant():
        cif = cif_entry.get()
        address = address_entry.get()
        name = name_entry.get()
        password = password_entry.get()
        municipality = municipality_combobox.get()
        tables = tables_entry.get()
        phone = phone_entry.get()
        new_restaurant = Restaurant(cif, address, name, password, municipality, tables, phone,"")
        print(
            f"Restaurante creado: {new_restaurant.name}, {new_restaurant.cif}, {new_restaurant.address}, {new_restaurant.municipality}, {new_restaurant.tables},{new_restaurant.phone}, {new_restaurant.password}",new_restaurant.description)
        return new_restaurant

    def validar_datos():
        errores = []
        cif = cif_entry.get()
        address = address_entry.get()
        name = name_entry.get()
        phone = phone_entry.get()
        municipality = municipality_combobox.get()
        tables = tables_entry.get()
        password = password_entry.get()
        resultado = True

        if not re.match(r"^[A-HJ-NP-SUVW]{1}\d{7}[0-9A-J]$", cif):
            errores.append(
                "El CIF debe empezar con una letra válida, seguido de 7 números y un dígito o letra de control(0-9 o A-J)")
            cif_entry.configure(border_color="red")
            resultado = False

        if not address:
            errores.append("La dirección no puede estar vacía.")
            address_entry.configure(border_color="red")
            resultado = False

        if not name:
            errores.append("El nombre no puede estar vacío.")
            name_entry.configure(border_color="red")
            resultado = False
        elif db.obtain_restaurant_name(name):
            errores.append("El nombre del restaurante ya está registrado, prueba con otro")
            name_entry.configure(border_color="red")
            resultado = False

        if not phone.isdigit() or len(phone) != 9:
            errores.append("El número de teléfono debe tener 9 números y solo debe contener números.")
            phone_entry.configure(border_color="red")
            resultado = False
        elif db.phone_exists(phone):
            errores.append("El número de teléfono ya esta en uso.")
            phone_entry.configure(border_color="red")
            resultado = False

        if not municipality:
            errores.append("Debe seleccionar un municipio.")
            resultado = False

        if not tables.isdigit() or int(tables) <= 0:
            errores.append("El número de mesas debe ser un número mayor que 0.")
            tables_entry.configure(border_color="red")
            resultado = False

        if not (len(password) >= 7 and re.search(r'\d', password) and re.search(r'[A-Z]', password)
                and re.search(r'[a-z]', password) and re.search(r'[@#$€]', password)):
            errores.append(
                "La contraseña debe tener al menos 7 caracteres, una letra mayúscula, una letra minúscula, un número y un carácter especial (@#$€).")
            password_entry.configure(border_color="red")
            resultado = False

        if resultado:
            if db.obtain_cif(cif):
                errores.append("El CIF ya está registrado.")
                BasicController.show_errors(errores)
            else:
                db.add_restaurant(create_restaurant())
                BasicController.usage_window("Registro exitosos", "Registro Completado")

                entries = [cif_entry, address_entry, name_entry, phone_entry, tables_entry, password_entry]
                for entry in entries:
                    entry.delete(0, "end")
                    entry.insert(0, "")

                # Resetear el combobox de municipio
                municipality_combobox.set("")
        else:
            BasicController.show_errors(errores)

    register_button = ctk.CTkButton(main_frame, text="Registrarse", command=validar_datos)
    register_button.grid(row=8, column=0, columnspan=2, pady=15)
    def on_register_button_enter(event):
        register_button.configure(cursor="hand2")

    def on_register_button_leave(event):
        register_button.configure(cursor="")

    register_button.bind("<Enter>", on_register_button_enter)
    register_button.bind("<Leave>", on_register_button_leave)

    def on_focus_in(event, widget):
        widget.configure(border_color="#1E90FF")

    def on_focus_out(event, widget):
        widget.configure(border_color="")

    def add_focus_effect_to_all_entries(container):
        for widget in container.winfo_children():
            if isinstance(widget, ctk.CTkEntry):
                widget.bind("<FocusIn>", lambda event, w=widget: on_focus_in(event, w))
                widget.bind("<FocusOut>", lambda event, w=widget: on_focus_out(event, w))
            elif widget.winfo_children():
                add_focus_effect_to_all_entries(widget)

    add_focus_effect_to_all_entries(main_frame)

    window.protocol("WM_DELETE_WINDOW", lambda: open_Login(window, db))
    window.attributes("-topmost", True)

    window.mainloop()


def open_Login(current_window, db):
    from Views.RestaurantLogin import open_restaurant_login_window

    current_window.destroy()
    open_restaurant_login_window(db)

if __name__ == "__main__":
    from Controllers import DataBaseController

    db = DataBaseController()
    db.open_connection()
    try:
        open_restaurant_registration_window(db,None)
    finally:
        db.close_connection()

