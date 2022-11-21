from flask import (Blueprint, current_app, flash, g, redirect, render_template,
                   request, session, url_for, abort)
from werkzeug.security import check_password_hash, generate_password_hash
from kgweb.db import db, User
import flask_login
import json
from . import Result

bp = Blueprint('manage', __name__)

@bp.route("/users", methods = ['POST', 'GET'])
@flask_login.login_required
def users():
    if flask_login.current_user.role != 'admin': return Result().unauthorized()
    if request.method == 'POST':
        if not request.is_json or not isinstance(request.json['page'], int) : return Result().fail('data error')
        # 分页，默认一页20个
        page =  db.paginate(db.select(User).order_by(User.id), page = request.json['page'], error_out=False)
        if len(page.items) == 0: return Result().empty()
        res = Result()
        # 参考 https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/api/#module-flask_sqlalchemy.pagination
        res['items'] = page.items
        res['page'] = page.page
        res['per_page'] = page.per_page
        res['total'] = page.total
        res['first'] = page.first
        res['last'] = page.last
        res['pages'] = page.pages
        res['has_prev'] = page.has_prev
        res['has_next'] = page.has_next
        res['prev_num'] = page.prev_num
        res['next_num'] = page.next_num
        res['iter_pages'] = list(page.iter_pages())
        return res.success()
    return render_template('manage/users.html')