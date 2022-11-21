import datetime
import logging
import os
import flask_login
from flask import (Flask, current_app, g, render_template, request,
                   send_from_directory, session)
from kgweb.Result import *


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # 配置，其中session过期时间为7天
    app.config.from_mapping(
        PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=7),
        SECRET_KEY='1fcea46a3e36a7416633efed7ed9a4605d69e7581b1a2cc67bd46ce8a78babf6',
        GRAPH_DATABASE='bolt://localhost:7687,neo4j,AAA200010199',
        DATABASE=os.path.join(app.instance_path, 'kgweb.sqlite'),
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user01:user01@localhost:3306/kgweb',
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        SQLALCHEMY_ECHO = True
    )

    # 加载配置文件
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 注册json方法
    from . import db
    app.json_provider_class = db.CustomJsonProvider
    app.json = db.CustomJsonProvider(app)

    # 注册db的方法
    db.init_app(app)

    # 注册auth蓝图
    from . import auth
    app.register_blueprint(auth.bp)
    from . import scale
    app.register_blueprint(scale.bp)
    from . import manage
    app.register_blueprint(manage.bp)
    
    #初始化登录管理器
    login_manager = flask_login.LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @app.route('/', methods = ['GET'])
    def index():
        return render_template('index.html.j2')

    @app.route('/favicon.ico')  # 设置icon
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),  # 对于当前文件所在路径,比如这里是static下的favicon.ico
                                   'favicon.ico', mimetype='type="image/x-icon"')
        
    #配置登录管理器
    @login_manager.user_loader
    def load_user(id):
        from .db import db, User
        return db.session.execute(db.select(User).where(User.id == id)).scalar_one_or_none()

    @app.post('/q')
    def query():
        """查询节点和关系接口
        参数形如{type:"xxx", prop:"xxx", keyword:"xxx"}
        """
        prop_map = {  # 属性名称的映射
            '按摩方法': {
                '主治': '名称'
            },
            '药材': {
                '名称': '中文名'
            }
        }
        des_map = {  # 每个类型对应需要放入des的属性
            '药材': ['功效', '别名', '归经', '性味'],
            '食疗食谱': ['主治', '做法', '应用分析', '用法'],
            '方剂': ['主治', '功效'],
            '按摩方法': ['按摩顺序与技法'],
            '穴位': ['主治', '取穴技巧', '经属', '自我按摩'],
            '疾病': ['疾病概述']
        }
        if request.is_json == False:
            return Result().fail('Not json')
        param = request.json
        current_app.logger.debug(request.json)
        pattern = f'.*?{param["key_word"]}.*?'
        prop = prop_map[param['type']][param['prop']] if prop_map.get(
            param['type'], None) is not None and prop_map[param['type']].get(param['prop'], None) is not None else param['prop']
        result = Result({"categories": list(),
                        "nodes": list(),
                         "edges": list()})
        categories = set()
        g = db.get_graph_db()
        sub_g = g.run(
            f'MATCH (a:{param["type"]})<-[r]->(b) WHERE a.{prop} =~ "{pattern}" return a, r, b').to_subgraph()
        if sub_g is None:
            return result.empty()
        for node in sub_g.nodes:
            n = dict(node)
            d = dict()
            d['id'] = n.pop("uuid")
            # 标签
            catg = list(node.labels)[0]
            categories.add(catg)
            d['category'] = catg
            d['name'] = n.get('中文名', None) if n.get(
                '中文名', None) is not None else n.get('名称', None)
            # 描述
            des_dict = dict()
            if des_map.get(catg, None) is not None:
                for k in des_map[catg]:
                    value = n.get(k, None)
                    if value is not None:
                        des_dict[k] = value
                d['des'] = des_dict
            else:
                d['des'] = n
            result['nodes'].append(d)
        for relation in sub_g.relationships:
            e = dict()
            e['source'] = relation.start_node['uuid']
            e['target'] = relation.end_node['uuid']
            des_dict = dict(relation)
            des_dict.pop('uuid', None)
            e['des'] = type(relation).__name__ + \
                (str(des_dict) if len(des_dict) != 0 else '')
            result['edges'].append(e)
        for c in categories:
            result['categories'].append({'name': c})
        logging.info(f'/q post val:{request.json}')
        return result.success()
    return app


# @app.route('/profile/<username>')
# def profile(username):
#     return f'{escape(username)}\'s profile'


# @app.post('/login/')
# def login():
#     return f'username:{request.form["username"]}\npassword:{request.form["password"]}'


# @app.get('/users/')
# def get_users():
#     return {
#         'username': 'tom',
#         'passwrod': '123456'
#     }
