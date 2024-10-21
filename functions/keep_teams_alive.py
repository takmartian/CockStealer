import threading
import pyautogui
import time
import random

kta_state = False

def keep_teams_alive():
    global kta_state
    while kta_state:
        x = random.randint(-1, 1)
        y = random.randint(-1, 1)
        pyautogui.move(x, y)
        time.sleep(10)

def toggle_kta(state: bool):
    global kta_state

    if state:
        kta_state = True
        threading.Thread(target=keep_teams_alive, daemon=True).start()
    else:
        kta_state = False