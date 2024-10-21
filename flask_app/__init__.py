from flask import Flask
from flask_cors import CORS

def create_flask_app():
    app = Flask(__name__)
    CORS(app)

    from .routes import main_routes  # 导入路由
    app.register_blueprint(main_routes)  # 注册蓝图

    return app