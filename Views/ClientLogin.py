import customtkinter as ctk
import os
from Controllers import DataBaseController,BasicController
from Views.ClientApp.ClientApp import main as client_app
from Views.ClientRegistration import open_client_registration_window


def open_client_login_window(db, event=None):
    window = ctk.CTk()
    window.title("Inicio de Sesión del Cliente")
    BasicController.center_window(window, 400, 390)
    window.resizable(False, False)

    window.iconbitmap(BasicController.obtain_icon_path())

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")


    BasicController.center_window(window, 400, 390)

    main_frame = ctk.CTkFrame(window, corner_radius=10)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True, side="left")

    title_label = ctk.CTkLabel(main_frame, text="Inicio de Sesión\nCliente", font=("Helvetica", 30), anchor='center')
    title_label.pack(pady=10)

    dni_label = ctk.CTkLabel(main_frame, text="Introduce el DNI:", font=("Helvetica", 18))
    dni_label.pack(pady=5)
    dni_entry = ctk.CTkEntry(main_frame, width=200, font=("Helvetica", 12), text_color="light grey")
    dni_entry.bind("<FocusIn>", lambda event: dni_entry.configure(border_color="#1E90FF"))
    dni_entry.bind("<FocusOut>", lambda event: dni_entry.configure(border_color=""))
    dni_entry.pack(pady=5)

    password_label = ctk.CTkLabel(main_frame, text="Introduce la contraseña:", font=("Helvetica", 18))
    password_label.pack(pady=5)
    password_entry = ctk.CTkEntry(main_frame, width=200, show='*', font=("Helvetica", 12), text_color="light grey")
    password_entry.pack(pady=5)
    password_entry.bind("<FocusIn>", lambda event: password_entry.configure(border_color="#1E90FF"))
    password_entry.bind("<FocusOut>", lambda event: password_entry.configure(border_color=""))


    def validation():
        dni = dni_entry.get()
        password = password_entry.get()
        result = True
        errors = []

        if db.obtain_dni(dni) != True:
            result = False
            dni_entry.configure(border_color="red")
            errors.append("El DNI no esta asignado a ningun usuario")
        else:
            if db.obtain_password_client(dni) != password:
                result = False
                errors.append("Esta contraseña no es la correcta")
        if result != True:
            BasicController.show_errors(errors)
        else:
            window.destroy()
            client_app(db,dni)

    login_button = ctk.CTkButton(main_frame, text="Iniciar Sesión", command=validation)
    login_button.pack(pady=10)
    login_button.bind("<Enter>", lambda event: login_button.configure(cursor="hand2"))
    login_button.bind("<Leave>", lambda event: login_button.configure(cursor=""))

    register_label = ctk.CTkLabel(main_frame, text="¿No te has registrado? Regístrate aquí",
                                  text_color="white")
    register_label.bind("<Button-1>", lambda event: [BasicController.cancel_all_events(window),window.destroy(),open_client_registration_window(db)])
    register_label.bind("<Enter>", lambda event: register_label.configure(text_color="#1E90FF", cursor="hand2"))
    register_label.bind("<Leave>", lambda event: register_label.configure(text_color="white", cursor=""))
    register_label.pack(pady=5)

    window.protocol("WM_DELETE_WINDOW", lambda: open_Inicio_on_close(window, db))
    window.attributes("-topmost", True)

    window.mainloop()


def open_Inicio_on_close(current_window, db):
    from Views.Inicio import main
    BasicController.cancel_all_events(current_window)
    current_window.destroy()
    main(db)

if __name__ == "__main__":
    db = DataBaseController()
    db.open_connection()
    try:
        open_client_login_window(db)
    finally:
        db.close_connection()