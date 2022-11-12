import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from kgweb.db import get_db

"""
登录验证蓝图，蓝图名称是auth，url的前缀是/auth
"""
bp = Blueprint('auth', __name__, url_prefix='/auth')