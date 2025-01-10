import customtkinter as ctk
from Controllers import BasicController
from Views.RestaurantApp import RestaurantApp
from Views.RestaurantRegistration import open_restaurant_registration_window

def open_restaurant_login_window(db, event=None):
    window = ctk.CTk()
    window.title("Inicio de Sesión del Restaurante")
    window.geometry("400x390")
    window.resizable(False, False)

    window.iconbitmap(BasicController.obtain_icon_path())

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    BasicController.center_window(window, 400, 390)

    main_frame = ctk.CTkFrame(window, corner_radius=10)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True, side="left")

    title_label = ctk.CTkLabel(main_frame, text="Inicio de Sesión\nRestaurante", font=("Helvetica", 30),
                               anchor='center')
    title_label.pack(pady=10)

    cif_label = ctk.CTkLabel(main_frame, text="Introduce el CIF:", font=("Helvetica", 18))
    cif_label.pack(pady=5)
    cif_entry = ctk.CTkEntry(main_frame, width=200, font=("Helvetica", 12), text_color="light grey")
    cif_entry.bind("<FocusIn>", lambda event: cif_entry.configure(border_color="#1E90FF"))
    cif_entry.bind("<FocusOut>", lambda event: cif_entry.configure(border_color=""))
    cif_entry.pack(pady=5)

    password_label = ctk.CTkLabel(main_frame, text="Introduce la contraseña:", font=("Helvetica", 18))
    password_label.pack(pady=5)
    password_entry = ctk.CTkEntry(main_frame, width=200, show='*', font=("Helvetica", 12), text_color="light grey")
    password_entry.bind("<FocusIn>", lambda event: password_entry.configure(border_color="#1E90FF"))
    password_entry.bind("<FocusOut>", lambda event: password_entry.configure(border_color=""))
    password_entry.pack(pady=5)

    def validation():
        cif = cif_entry.get()
        password = password_entry.get()
        result = True
        errors = []

        if db.obtain_cif(cif) != True:
            result = False
            cif_entry.configure(border_color="red")
            errors.append("El CIF no está asignado a ningún restaurante.")
        else:
            if db.obtain_password_restaurant(cif) != password:
                result = False
                errors.append("La contraseña no es correcta.")

        if result != True:
            BasicController.show_errors(errors)
        else:
            window.destroy()
            RestaurantApp.main(db, cif)

    login_button = ctk.CTkButton(main_frame, text="Iniciar Sesión", command=validation)
    login_button.pack(pady=10)

    # Añadir la funcionalidad para que se pulse el botón de inicio de sesión al presionar Enter
    cif_entry.bind("<Return>", lambda event: validation())
    password_entry.bind("<Return>", lambda event: validation())

    register_label = ctk.CTkLabel(main_frame, text="¿No te has registrado? Regístrate aquí", text_color="white")
    register_label.pack(pady=5)

    register_label.bind("<Button-1>", lambda event: [BasicController.cancel_all_events(window), window.destroy(),
                                                     open_restaurant_registration_window(db)])
    register_label.bind("<Enter>", lambda event: register_label.configure(text_color="#1E90FF", cursor="hand2"))
    register_label.bind("<Leave>", lambda event: register_label.configure(text_color="white", cursor=""))

    window.protocol("WM_DELETE_WINDOW", lambda: open_Inicio_on_close(window, db))
    window.attributes("-topmost", True)
    window.mainloop()

def open_Inicio_on_close(current_window, db):
    from Views.Inicio import main
    BasicController.cancel_all_events(current_window)
    current_window.destroy()
    main(db)

if __name__ == "__main__":
    from Controllers import DataBaseController

    db = DataBaseController()
    db.open_connection()
    try:
        open_restaurant_login_window(db, None)
    finally:
        db.close_connection()


