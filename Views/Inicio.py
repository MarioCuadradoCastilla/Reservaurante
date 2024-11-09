import customtkinter
from PIL import Image, ImageTk  # Importar Image y ImageTk
from InicioSesionCliente import open_client_login_window  
from inicioSesionRestaurante import open_restaurant_login_window

# Configuración de apariencia y tema
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# Crear la ventana principal
root = customtkinter.CTk()
root.title("Reservaurante")
root.iconbitmap("./img/icono.ico")

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

# Crear un marco dentro de la ventana
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=30, fill="both", expand=True)

# Cargar la imagen y especificar el tamaño
image_path = "./img/icono2.png"  # Cambia a la ruta de tu imagen
image = customtkinter.CTkImage(light_image=Image.open(image_path),size=(220,220))
image_label=customtkinter.CTkLabel(master=frame,image=image,text='')
image_label.place(y=20,x=95)

label_bienvenido = customtkinter.CTkLabel(
    master=frame,
    text="Reservaurante",
    font=("Roboto", 48, "bold"),  # Fuente, tamaño y estilo
    text_color="#3DA5E0"
)
label_bienvenido.pack(pady=240, padx=12)

def create_hover_label(master, text, x, y,onClick):
    label = customtkinter.CTkLabel(
        master=master,
        text=text,
        font=("Roboto", 20, "normal"),
        text_color="white"  # Color inicial del texto
    )
    label.place(x=x, y=y)

    # Funciones para cambiar el color del texto
    def on_enter(event):
        label.configure(text_color="#3DA5E0")  # Cambia a amarillo al pasar el ratón

    def on_leave(event):
        label.configure(text_color="white")  # Vuelve a blanco al salir

    # Asociar eventos de ratón con las funciones
    label.bind("<Enter>", on_enter)
    label.bind("<Leave>", on_leave)
    label.bind("<Button-1>", onClick)  # Llama a la función cuando se hace clic
    return label

# Crear varios labels con diferentes funciones de clic
label1 = create_hover_label(frame, "Iniciar sesión como cliente", 75, 350, open_client_login_window)
label2 = create_hover_label(frame, "Iniciar sesión como restaurante", 55, 410, open_restaurant_login_window)

root.mainloop()




    