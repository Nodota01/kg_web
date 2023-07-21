from flask import (Blueprint, current_app, render_template,
                   request)
from . import Result, model_assert

bp = Blueprint('chat', __name__)

@bp.route("/chat", methods = ['GET'])
def chat():
    return render_template('chat.html')