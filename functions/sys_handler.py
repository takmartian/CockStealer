import sys
import os

# 判断是否为冻结程序
def is_frozen():
    return getattr(sys, 'frozen', False)

# 获取当前系统类型
def get_system_type():
    return os.name