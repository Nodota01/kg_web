import json
import os
from kgweb.db import db
from flask import (Blueprint, current_app, flash, g, redirect, render_template,
                   request, session, url_for)
import flask_login

from . import Result

bp = Blueprint('scale', __name__)

@bp.route("/scale/<scale_name>")
@flask_login.login_required
def scale(scale_name):
    g.scale_name = scale_name
    try:
        with open(os.path.join(current_app.root_path, f'static/data/scales/{scale_name}_scale.json') , mode='r', encoding='utf8') as f:
            scale_data = json.loads(f.read())
            g.scale_data = scale_data
    except OSError as e:
        current_app.logger.error(e)
    else:
        return render_template('scale/base.html.j2')
    # 找不到量表回到主页
    return redirect(url_for('index'))