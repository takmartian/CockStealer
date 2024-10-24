import sys
import os

# 判断是否为冻结程序
def is_frozen():
    return getattr(sys, 'frozen', False)

# 获取当前系统类型
def get_system_type():
    return os.name

# 获取静态资源文件夹
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

# 设置全局变量
def set_global_var(name: str, value):
    globals()[name] = value

# 获取全局变量
def get_global_var(name: str):
    return globals().get(name)


# 退出程序
def exit_program():
    sys.exit(0)
