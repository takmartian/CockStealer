from flask import Blueprint, render_template, request, send_from_directory
from functions.dingtalk_js_generator import DingTalkJSGenerator

main_routes = Blueprint('main', __name__)


@main_routes.route('/gen_autoxjs', methods=['GET'])
def gen_autoxjs():
    return render_template('gen_autoxjs.html')


@main_routes.route('/dingtalk_js', methods=['POST'])
def dingtalk_js():
    print(request.json)
    dtg = DingTalkJSGenerator(request.json)
    result = dtg.gen_dingtalk_js()
    return result


@main_routes.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)
