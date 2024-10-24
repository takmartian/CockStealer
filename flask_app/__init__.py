from flask import Flask
from flask_cors import CORS
from sys_handler import set_global_var
from gevent import pywsgi

import functions.network_handler as network_handler

def create_flask_app():
    app = Flask(__name__)
    CORS(app)

    from .routes import main_routes  # 导入路由
    app.register_blueprint(main_routes)  # 注册蓝图

    return app


def main():
    app = create_flask_app()
    # 生成随机端口
    port = network_handler.get_random_port()
    set_global_var('flask_port', port)

    server = pywsgi.WSGIServer(('0.0.0.0', port), app)
    server.serve_forever()
