import sys
import os


def is_frozen():
    """
    判断是否为冻结程序（已打包）
    :return:
    """
    return getattr(sys, 'frozen', False)


def get_system_type():
    """
    获取当前系统类型
    :return: 系统类型
    """
    return os.name


def get_static_folder(path: str):
    """
    获取静态资源文件夹
    :param path: 静态资源文件夹路径
    :return: 完整静态资源文件夹路径
    """
    if is_frozen():
        return os.path.join(sys._MEIPASS, path)
    else:
        return os.path.join(os.path.dirname(__file__), path)


def set_global_var(name: str, value):
    """
    设置全局变量
    :param name: 全局变量名称
    :param value: 全局变量值
    """
    globals()[name] = value


# 获取全局变量
def get_global_var(name: str):
    """
    获取全局变量
    :param name: 全局变量名称
    :return: 全局变量值
    """
    return globals().get(name)


# 退出程序
def exit_program():
    sys.exit(0)
