from flask import (Blueprint, current_app, flash, g, redirect, render_template,
                   request, session, url_for, abort)
from werkzeug.security import check_password_hash, generate_password_hash
from kgweb.db import db, User
import flask_login
import json
import re
import logging
from . import Result, model_assert

bp = Blueprint('herb_recommend', __name__)

@bp.route("/get_herbs", methods = ['GET', 'POST'])
@flask_login.login_required
def herb_recommend():
    if(request.method == 'GET'):
        pass
    elif(request.method == 'POST'):
        if not request.is_json or not isinstance(request.json['symps'], list) : 
            return Result().fail('data error')
        if isinstance(request.json['k'], int):
            return Result(model_assert.model_loader.get_recommend_herb(request.json['symps'], k = request.json['k'])).success()
        else:
            return Result(model_assert.model_loader.get_recommend_herb(request.json['symps'])).success()