from flask import (Blueprint, current_app, flash, g, redirect, render_template,
                   request, session, url_for, abort)
from werkzeug.security import check_password_hash, generate_password_hash
from kgweb.db import db, User
import flask_login
import json
import re
from . import Result

bp = Blueprint('user', __name__)

@bp.before_request
def varify_auth():
    '''验证权限，返回后所请求的方法将不会再被执行
    '''
    if flask_login.current_user.role != 'admin': return Result().unauthorized()

@bp.route("/user", methods = ['GET', 'POST'])
@flask_login.login_required
def user():
    if request.method == 'POST':
        if not request.is_json or not isinstance(request.json['page'], int) : return Result().fail('data error')
        # 查询分页，默认一页20个
        query_type = request.json['query_type']
        query_data = request.json['query_data']
        if query_type is None or query_data is None or query_type not in ['id', 'name', 'phone']:
            page = db.paginate(db.select(User).order_by(User.id), page = request.json['page'], error_out=False)
        elif query_type == 'id':
            if not isinstance(query_data, int) and not re.match(r'\d+', query_data): return Result().empty()
            page = db.paginate(db.select(User).where(User.id == int(query_data)).order_by(User.id), page = request.json['page'], error_out=False)
        elif query_type == 'name':
            page = db.paginate(db.select(User).where(User.name.like(f'%{query_data}%')).order_by(User.id), page = request.json['page'], error_out=False)
        elif query_type == 'phone':
            page = db.paginate(db.select(User).where(User.phone.like(f'%{query_data}%')).order_by(User.id), page = request.json['page'], error_out=False)
        if len(page.items) == 0: return Result().empty()
        res = Result(page = page)
        # 参考 https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/api/#module-flask_sqlalchemy.pagination
        return res.success()
    return render_template('manage/users.html')
    