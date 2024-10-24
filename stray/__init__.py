import pystray
from pystray import Menu, MenuItem as Item
from PIL import Image

import functions.keep_teams_alive as kta


kta_state = False

def about_this(icon: pystray.Icon):
    icon.notify(title='关于', message='本软件仅用于学习用途，并不对任何使用者的行为负责')


def on_quit(stray, item):
    stray.stop()


def keep_teams_alive(icon, item):
    global kta_state
    kta_state = not item.checked

    if kta_state:
        kta.toggle_kta(True)
    else:
        kta.toggle_kta(False)


# 打开网页http://127.0.0.1:5200/gen_autoxjs
def open_gen_autoxjs(icon, item):
    import webbrowser
    webbrowser.open('http://127.0.0.1:5200/gen_autoxjs')


def initial_stray():
    image = Image.open('./images/tray_icon.ico')
    menu = Menu(
        Item('保持Teams在线', action=keep_teams_alive, checked=lambda item: kta_state),
        Item('钉钉打卡脚本', action=open_gen_autoxjs),
        Item('帮助', Menu(
            Item('关于本软件', action=about_this),
            Item('版本号: v0.2.0', action=None, enabled=False)
            )
        ),
        Item('退出', on_quit),
    )

    stray = pystray.Icon('StealCock偷鸡工具包', image, 'StealCock偷鸡工具包', menu)
    stray.run()