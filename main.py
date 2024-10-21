import logging
import threading
from logging.handlers import RotatingFileHandler

from functions.sys_handler import get_system_type, is_frozen
from flask_app import create_flask_app
from stray import initial_stray


# 创建日志处理器，日志文件最大为 1MB，最多保留 1 个备份文件
handler = RotatingFileHandler('app.log', maxBytes=2 * 1024 * 1024, backupCount=1)

# 在项目主入口文件中配置 logging
logging.basicConfig(
    level=logging.INFO if is_frozen() else logging.DEBUG,  # 日志级别，冻结时为INFO，否则为DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 日志格式
    handlers=[
        handler,
        logging.StreamHandler()
    ]
)

# 运行flask
def run_flask():
    flask_app = create_flask_app()
    flask_app.run(host='0.0.0.0', port=5200)


def main():
    # 创建线程运行flask
    threading.Thread(target=run_flask, daemon=True).start()

    # 初始化托盘
    initial_stray()


if __name__ == '__main__':
    main()