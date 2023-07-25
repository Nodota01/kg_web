from flask import (Blueprint, current_app, render_template,
                   request, send_file)
from . import Result, model_assert

bp = Blueprint('chat', __name__)

@bp.route("/chat", methods = ['GET'])
def chat():
    # 无需经过模板引擎渲染，否则VUE失效
    return send_file('templates/chat.html')