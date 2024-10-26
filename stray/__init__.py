import pystray
from pystray import Menu, MenuItem as Item
from PIL import Image

import functions.keep_teams_alive as kta
from sys_handler import get_global_var, exit_program, get_static_folder

# 初始化保持Teams在线状态
kta_state = False


def about_this(icon: pystray.Icon):
    # 关于
    icon.notify(title='关于', message='本软件仅用于学习用途，并不对任何使用者的行为负责')


def on_quit(stray, item):
    # 退出程序
    stray.stop()
    exit_program()


def keep_teams_alive(icon, item):
    """
    保持Teams在线
    """
    global kta_state

    # 切换状态
    kta_state = not item.checked

    if kta_state:
        # 开启保持Teams在线
        kta.toggle_kta(True)
    else:
        # 关闭保持Teams在线
        kta.toggle_kta(False)


def open_gen_autoxjs(icon, item):
    """
    打开钉钉打卡脚本生成页面
    """
    import webbrowser
    port = get_global_var('flask_port')
    webbrowser.open(f'http://127.0.0.1:{port}/gen_autoxjs')


def initial_stray():
    """
    初始化托盘
    """
    image = Image.open(get_static_folder('images/tray_icon.ico'))
    menu = Menu(
        Item('保持Teams在线', action=keep_teams_alive, checked=lambda item: kta_state),
        Item('钉钉打卡脚本', action=open_gen_autoxjs),
        Item('帮助', Menu(
            Item('关于本软件', action=about_this),
            Item('版本号: v0.3.9', action=None, enabled=False)
        )
             ),
        Item('退出', on_quit),
    )

    stray = pystray.Icon('StealCock偷鸡工具包', image, 'StealCock偷鸡工具包', menu)
    stray.run()
