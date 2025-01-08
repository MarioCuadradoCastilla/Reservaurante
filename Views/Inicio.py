import customtkinter as ctk
from PIL import Image
from Views.RestaurantLogin import open_restaurant_login_window
from Views.ClientLogin import open_client_login_window
from Controllers import DataBaseController, BasicController
import os


def main(db):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    db = DataBaseController()
    db.create_tables_if_not_exists()

    window = ctk.CTk()
    window.resizable(False, False)
    window.title("Reservaurante")

    window.iconbitmap(BasicController.obtain_icon_path())

    BasicController.center_window(window,450,600)

    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)

    frame = ctk.CTkFrame(master=window)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.rowconfigure(1, weight=1)
    frame.columnconfigure(0, weight=1)

    image_path = os.path.join(BasicController.obtain_script_dir(), "..", "img", "icono2.png")
    if os.path.exists(image_path):
        image = ctk.CTkImage(light_image=Image.open(image_path), size=(220, 220))
        image_label = ctk.CTkLabel(master=frame, image=image, text='')
        image_label.grid(row=0, column=0, pady=(30, 0), sticky="n")
    else:
        print(f"Error: El archivo {image_path} no se encontró.")

    label_welcome = ctk.CTkLabel(
        master=frame,
        text="Reservaurante",
        font=("Roboto", 36, "bold"),
        text_color="#1E90FF"
    )
    label_welcome.grid(row=1, column=0, pady=(40, 0), sticky="n")

    register_client_label = ctk.CTkLabel(
        frame,
        text="Inicia sesión como cliente",
        text_color="white",
        font = ("Helvetica", 22)
    )
    register_client_label.bind("<Button-1>", lambda event: [BasicController.cancel_all_events(window),window.destroy(), open_client_login_window(db)])
    register_client_label.bind("<Enter>", lambda event: register_client_label.configure(text_color="#1E90FF", cursor="hand2"))
    register_client_label.bind("<Leave>", lambda event: register_client_label.configure(text_color="white", cursor=""))
    # Usamos grid en lugar de pack
    register_client_label.grid(row=2, column=0, pady=1, sticky="n")

    register_restaurant_label = ctk.CTkLabel(
        frame,
        text="Inicia sesión como Restaurante",
        text_color="white",
        font = ("Helvetica", 22)
    )
    register_restaurant_label.bind("<Button-1>", lambda event: [BasicController.cancel_all_events(window) ,window.destroy(), open_restaurant_login_window(db)])
    register_restaurant_label.bind("<Enter>", lambda event: register_restaurant_label.configure(text_color="#1E90FF",cursor="hand2"))
    register_restaurant_label.bind("<Leave>", lambda event: register_restaurant_label.configure(text_color="white", cursor=""))

    register_restaurant_label.grid(row=2, column=0, pady=40, sticky="n")

    frame.pack(pady=20, padx=30, fill="both", expand=True)

    window.mainloop()

    db.close_connection()

if __name__ == '__main__':
    while True:
        main(None)
        break
