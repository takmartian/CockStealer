import socket


def check_port(port):
    """
    检查端口是否被占用
    :param port: 端口号
    :return: bool
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(('0.0.0.0', port))
        s.close()
        return True
    except OSError:
        return False


def get_random_port():
    """
    获取随机端口
    :return: int
    """
    import random
    port = random.randint(5200, 5299)
    while not check_port(port):
        port = random.randint(5000, 6000)


    return port