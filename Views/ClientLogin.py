# clientLogin.py
import customtkinter

def open_client_login_window(Event=None):
    login_window = customtkinter.CTk()
    login_window.title("Iniciar Sesión")
    login_window.geometry("300x200")
    
    label = customtkinter.CTkLabel(master=login_window, text="Esta es la ventana de inicio de sesión del client.")
    label.pack(pady=20)

     # Asegura que la ventana tenga el foco y que el usuario no pueda interactuar con la ventana principal
    login_window.grab_set()  # Establece el grab en esta ventana
    login_window.focus_force()  # Asegura que la ventana tenga el foco
    login_window.mainloop()