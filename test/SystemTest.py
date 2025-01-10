import sys
import os
import pyautogui
import time
import threading
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Views.ClientLogin import open_client_login_window
from Controllers.DataBaseController import DataBaseController

def perform_gui_automation():
    time.sleep(5)
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.write('12345678A')
    time.sleep(1)
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.write('Pass123')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'alt', '2')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    time.sleep(5)
    print("Login Test Passed")

def test_login():
    db = DataBaseController()
    db.open_connection()
    try:
        automation_thread = threading.Thread(target=perform_gui_automation)
        automation_thread.start()
        open_client_login_window(db)
        automation_thread.join()
    except Exception as e:
        print(f"Error durante la prueba: {e}")
    finally:
        db.close_connection()
        print("Conexión a la base de datos cerrada.")

if __name__ == "__main__":
    test_login()
