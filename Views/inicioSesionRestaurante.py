# inicioSesionCliente.py
import customtkinter

def open_restaurant_login_window(event=None):
    registration_window = customtkinter.CTk()
    registration_window.title("Registro")
    registration_window.geometry("300x200")
    
    label = customtkinter.CTkLabel(master=registration_window, text="Esta es la ventana de inicio de sesion del restaurante.")
    label.pack(pady=20)

    registration_window.grab_set()
    registration_window.focus_force()  # Asegura que la ventana tenga el foco
    registration_window.mainloop() # Iniciar el bucle principal para la nueva ventana
