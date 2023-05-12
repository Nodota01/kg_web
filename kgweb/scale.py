import json
import os
from flask import (Blueprint, current_app, redirect, render_template,
                   request, url_for)
import flask_login

from . import Result

bp = Blueprint('scale', __name__)

@bp.get("/scale/<scale_name>")
@flask_login.login_required
def scale(scale_name):
    try:
        with open(os.path.join(current_app.root_path, f'static/data/scales/{scale_name}_scale.json') , mode='r', encoding='utf8') as f:
            scale_data = json.loads(f.read())
            scale_data['en_name'] = scale_name
    except OSError as e:
        current_app.logger.error(e)
    else:
        return render_template('scale/base.html.j2', scale_data = scale_data)
    # 找不到量表回到主页
    return redirect(url_for('index'))

@bp.post("/scale/judge")
@flask_login.login_required
def judge():
    if not request.is_json or request.json['scale_name'] is None or request.json['items'] is None: return Result().fail('request data error')
    
