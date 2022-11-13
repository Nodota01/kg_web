import functools
from . import Result
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash
from kgweb.db import get_db

"""
登录验证蓝图，蓝图名称是auth，url的前缀是/auth
"""
bp = Blueprint('auth', __name__)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
    注册
    GET请求获取网页
    POST请求为注册接口
    """
    if request.method == 'POST':
        phone = request.json['phone']
        password = request.json['password']
        current_app.logger.debug(request.json)
        db = get_db()
        error = None
        if not phone:
            error = 'Phone number is required.'
        elif not password:
            error = 'Password is required.'
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (phone, password) VALUES (?, ?)",
                    (phone, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Phone number {phone} is already registered."
            else:
                return Result().success()
        return Result().fail(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    登录
    GET请求获取网页
    POST请求为登录接口
    """
    if request.method == 'POST':
        phone = request.json['phone']
        password = request.json['password']
        current_app.logger.debug(request.json)
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE phone = ?', (phone,)
        ).fetchone()

        if user is None:
            error = 'Incorrect phone number.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return Result().success()
        else:
            return Result().fail(error)

    return render_template('auth/login.html')

@bp.post('/isLogin')
def is_login():
    """
    验证是否登录
    """
    res = Result()
    current_app.logger.debug(f'user:{g.user["name"]} is login' if g.user is not None else 'not login')
    res['isLogin'] = g.user is not None
    return res.success()

@bp.before_app_request
def load_logged_in_user():
    """
    在该蓝图所有方法执行前检查id
    并将用户存入g
    """
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        
@bp.route('/logout')
def logout():
    """
    退出登录
    """
    session.clear()
    return redirect(url_for('index'))