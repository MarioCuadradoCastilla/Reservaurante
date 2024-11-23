import os
import customtkinter
from PIL import Image, ImageTk
from ClientLogin import open_client_login_window  
from RestaurantLogin import open_restaurant_login_window

# Configuración de apariencia y tema
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# Crear la ventana principal
root = customtkinter.CTk()
root.title("Reservaurante")

# Obtener la ruta del script en ejecución
script_dir = os.path.dirname(os.path.abspath(__file__))

# Ruta relativa de la imagen del icono basada en la ruta del script
icon_path = os.path.join(script_dir, "..", "img", "icono.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)
else:
    print(f"Error: El archivo {icon_path} no se encontró.")

# Función para centrar la ventana
def center_window():
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 450
    window_height = 600
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

center_window()

# Configurar redimensionamiento para que se ajuste
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Crear un marco dentro de la ventana
frame = customtkinter.CTkFrame(master=root)
frame.grid(row=0, column=0, sticky="nsew")  # Usar grid para que se ajuste
frame.rowconfigure(1, weight=1)
frame.columnconfigure(0, weight=1)

# Cargar la imagen y especificar el tamaño
image_path = os.path.join(script_dir, "..", "img", "icono2.png")
if os.path.exists(image_path):
    image = customtkinter.CTkImage(light_image=Image.open(image_path), size=(220, 220))
    image_label = customtkinter.CTkLabel(master=frame, image=image, text='')
    image_label.grid(row=0, column=0, pady=(30, 0), sticky="n")  # Usar grid y sticky para ajustar posición
else:
    print(f"Error: El archivo {image_path} no se encontró.")

label_welcome = customtkinter.CTkLabel(
    master=frame,
    text="Reservaurante",
    font=("Roboto", 36, "bold"),
    text_color="#3DA5E0"
)
label_welcome.grid(row=1, column=0, pady=(40, 0), sticky="n")

def create_hover_label(master, text, onClick):
    label = customtkinter.CTkLabel(
        master=master,
        text=text,
        font=("Roboto", 20),
        text_color="white"
    )

    # Funciones para cambiar el color del texto al pasar el ratón
    def on_enter(event):
        label.configure(text_color="#3DA5E0")

    def on_leave(event):
        label.configure(text_color="white")

    # Asociar eventos de ratón con las funciones
    label.bind("<Enter>", on_enter)
    label.bind("<Leave>", on_leave)
    label.bind("<Button-1>", onClick)  # Llama a la función cuando se hace clic
    return label

# Crear varios labels con diferentes funciones de clic
label1 = create_hover_label(frame, "Iniciar sesión como cliente", open_client_login_window)
label1.grid(row=2, column=0, pady=(10, 10), sticky="ew")  # Ajusta pady para mover hacia arriba

label2 = create_hover_label(frame, "Iniciar sesión como restaurante", open_restaurant_login_window)
label2.grid(row=3, column=0, pady=(5, 20), sticky="ew")  # Ajusta pady para mover hacia arriba

# Ajustar el padding en el frame y configurar que ocupe toda la pantalla
frame.pack(pady=20, padx=30, fill="both", expand=True)

root.mainloop()

