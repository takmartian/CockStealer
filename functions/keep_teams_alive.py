import threading
import pyautogui
import time
import random

kta_state = False


def keep_teams_alive():
    """
    保持Teams在线
    """
    global kta_state

    # 随机移动鼠标
    while kta_state:
        x = random.randint(-1, 1)
        y = random.randint(-1, 1)
        pyautogui.move(x, y)
        time.sleep(10)


def toggle_kta(state: bool):
    global kta_state

    if state:
        # 开启保持Teams在线
        kta_state = True
        # 创建线程运行保持Teams在线
        threading.Thread(target=keep_teams_alive, daemon=True).start()
    else:
        # 关闭保持Teams在线
        kta_state = False
