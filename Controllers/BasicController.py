import json
import customtkinter as ctk
from tkinter import  TclError
import os

class BasicController:

    @staticmethod
    def center_window(window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (width / 2))
        y_cordinate = int((screen_height / 2) - (height / 2))
        window.geometry(f"{width}x{height}+{x_cordinate}+{y_cordinate}")

    @staticmethod
    def show_errors(errores):
        error_window = ctk.CTkToplevel()
        error_window.title("Error")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")


        error_window.grab_set()
        error_window.focus_force()
        error_window.attributes("-topmost", True)


        error_window_width = 450
        error_window_height = 250

        BasicController.center_window(error_window, error_window_width, error_window_height)

        error_window.resizable(False, False)
        error_window.configure(bg="dark")


        error_label = ctk.CTkLabel(error_window, text="Error", font=("Helvetica", 16), text_color="red", height=10)
        error_label.pack(pady=10)


        scrollable_frame = ctk.CTkScrollableFrame(error_window, width=320, height=230)  # Ajustar el tamaño si es necesario
        scrollable_frame.pack(pady=1, padx=10, fill="both", expand=True)


        error_text = "\n\n".join(errores)
        error_message = ctk.CTkLabel(scrollable_frame, text=error_text, font=("Helvetica", 13), text_color="white", justify="left", wraplength=300)
        error_message.pack(pady=10, padx=10)

        close_button = ctk.CTkButton(scrollable_frame, text="Cerrar", command=lambda: [error_window.grab_release(), error_window.destroy()])
        close_button.pack(pady=10)

    @staticmethod
    def usage_window(text1,text2):
            exito_window = ctk.CTkToplevel()
            exito_window.title(text1)

            BasicController.center_window(exito_window, 350, 200)

            exito_window.resizable(False, False)
            exito_window.configure(bg="#2d2d2d")

            exito_window.grab_set()
            exito_window.focus_force()
            exito_window.attributes("-topmost", True)

            exito_label = ctk.CTkLabel(exito_window, text=text2, font=("Helvetica", 16), text_color="green", height=10)
            exito_label.pack(pady=30)

            close_button = ctk.CTkButton(exito_window, text="Cerrar",command=lambda: [exito_window.grab_release(), exito_window.destroy()])
            close_button.pack(pady=10)


    @staticmethod
    def complete_destruction_and_transition(window, callback):
        BasicController.cancel_after_scripts(window)
        BasicController.unbind_all_events(window)
        window.destroy()
        callback()
    @staticmethod
    def cancel_after_scripts(window):
        try:
            scripts = window.tk.eval('after info').split()
            for script in scripts:
                try:
                    window.after_cancel(script)
                except TclError:
                    print("Error Tcl")
        except Exception as e:
                print(f'Eventos que no pueden ser cancelados: {e}')
    @staticmethod
    def unbind_all_events(widget):
        widget.unbind("<Button-1>")
        widget.unbind("<Enter>")
        widget.unbind("<Leave>")

    @staticmethod
    def load_municipalities():
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "..", "Data", "Municipality","Municipalities.json")
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data["municipios"]
    
    @staticmethod
    def obtain_icon_path():
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "..", "img", "icono.ico")
        if os.path.exists(icon_path):
            return icon_path
        else:
            print(f"Error: El archivo {icon_path} no se encontró.")

    @staticmethod
    def obtain_script_dir():
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return script_dir





