from flask import (Blueprint, current_app, flash, g, redirect, render_template,
                   request, session, url_for, abort)
from werkzeug.security import check_password_hash, generate_password_hash
from kgweb.db import db, User
import flask_login
from . import Result


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
        if request.is_json == False : return Result().fail('Not json')
        user = User(
                phone = request.json['phone'],
                name = request.json['name'],
                password = request.json['password'],
                age = request.json['age'],
                gender = request.json['gender'],
                email = request.json['email'],
                address = request.json['address']
        )
        current_app.logger.debug(request.json)
        error = None
        if not user.phone:
            error += 'Phone number is required.'
        elif db.session.execute(db.select(User).where(User.phone == user.phone)).scalar_one_or_none() is not None:
            error += f"电话号码{user.phone}已被注册"
        if not user.password:
            error += 'Password is required.'
        if not user.name:
            error += 'Name is required.'
        if not user.age:
            error += 'Age is required.'
        elif not isinstance(user.age, int):
            error += 'Age type error'
        elif user.age <= 0 or user.age >= 110:
            error += 'Age range error'
        if not user.gender:
            error += 'Gender is required.'
        if error is None:
            user.password = generate_password_hash(user.password)
            db.session.add(user)
            db.session.commit()
            return Result().success()
        return Result().fail(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    登录
    GET请求获取网页
    POST请求为登录接口：成功返回用户名
    """
    if request.method == 'POST':
        if request.is_json == False : return Result().fail('Not json')
        phone = request.json['phone']
        password = request.json['password']
        current_app.logger.debug(request.json)
        error = None
        user = db.session.execute(db.select(User).where(User.phone == phone)).scalar_one_or_none()
        print(user)
        if user is None:
            error = '账号不存在或电话号码错误'
        elif not check_password_hash(user.password, password):
            error = '密码错误'
        if error is None:
            res = Result({'name':user.name})
            flask_login.login_user(user)
            return res.success()
        else:
            return Result().fail(error)
    return render_template('auth/login.html')

@bp.route('/info', methods=('GET', 'POST'))
@flask_login.login_required
def info():
    if request.method == 'POST':
        user = {
            'phone' : flask_login.current_user.phone,
            'name' : flask_login.current_user.name,
            'age' : flask_login.current_user.age,
            'gender' : flask_login.current_user.gender,
            'email' : flask_login.current_user.email,
            'address' : flask_login.current_user.address
        }
        return Result(user).success()
    else:
        return render_template('auth/info.html')


@bp.post('/isLogin')
def is_login():
    """
    验证是否登录
    """
    res = Result()
    res['isLogin'] = flask_login.current_user.is_authenticated
    if res['isLogin']:
        res['name'] = flask_login.current_user.name
    return res.success()
    
@bp.route('/logout')
@flask_login.login_required
def logout():
    """
    退出登录
    """
    session.clear()
    flask_login.logout_user()
    return redirect(url_for('index'))
