import click
import py2neo as neo
import flask_login
import json
import flask
from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

"""
该文件封装了所有数据库的连接
g是一个特殊对象，对于每个请求都是唯一的。它用于存储在请求期间可能被多个函数访问的数据。get_db如果在同一请求中第二次调用该连接，则该连接将被存储和重用，而不是创建新连接。
current_app是另一个特殊对象，它指向处理请求的 Flask 应用程序。由于您使用了应用程序工厂，因此在编写其余代码时没有应用程序对象。 get_db将在应用程序创建并正在处理请求时调用，因此current_app可以使用。
"""

db = SQLAlchemy()


def init_app(app):
    """注册会话结束后摧毁数据库连接，注册命令
    """
    app.teardown_appcontext(close_all_db)
    app.cli.add_command(init_db_command)
    # 初始化SQLAlchemy
    db.init_app(app)


class User(db.Model, flask_login.UserMixin):
    __tablename__ = 'user'  # 设置表名, 表名默认为类名小写
    id = db.Column(db.Integer, primary_key=True)  # 设置主键, 默认自增
    phone = db.Column(db.String(32), unique=True,
                      nullable=False, index=True)  # 设置唯一约束和索引
    name = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(128))
    address = db.Column(db.Text)
    role = db.Column(db.String(32), nullable=False, default='user')
    created = db.Column(db.DateTime, default=datetime.now())

    def getdict(self) -> dict:
        return {
            'id': self.id,
            'phone': self.phone,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'email': self.email,
            'address': self.address,
            'role': self.role,
            'created': self.created
        }


# 自定义flask的json编码器
class CustomJsonProvider(flask.json.provider.JSONProvider):
    # 自定义json编码器
    class CustomJsonEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, User):
                return obj.getdict()
            if isinstance(obj, datetime):
                return obj.isoformat(' ')
            # Let the base class default method raise the TypeError
            return json.JSONEncoder.default(self, obj)

    def dumps(self, obj, **kwargs) -> str:
        return json.dumps(obj, cls=self.CustomJsonEncoder, ensure_ascii=True)

    def loads(self, s, **kwargs):
        return json.loads(s)


def get_graph_db():
    '''获取图数据库连接
    '''
    if 'graph_db' not in g:
        _res = current_app.config['GRAPH_DATABASE'].split(',')
        g.graph_db = neo.Graph(_res[0], auth=(_res[1], _res[2]))
    return g.graph_db

# def get_db():
#     if 'db' not in g:
#         # g.db = sqlite3.connect(
#         #     current_app.config['DATABASE'],
#         #     detect_types=sqlite3.PARSE_DECLTYPES
#         # )
#         # g.db.row_factory = sqlite3.Row
#         g.db = db.session
#     return g.db


def init_db():
    """初始化数据库，读取sql文件并执行
    """
    db.drop_all()
    db.create_all()
    users = [
        User(
        phone='17688888888',
        name='纯平',
        password='pbkdf2:sha256:260000$aDGiF8hQNDkHWtzz$80f75b5c1f286bba110476de4b75fe63e557720bf1805cb443881d2837ad4806',
        age=24,
        gender='男',
        email='admin@kgweb.com',
        role='admin',
        address='古龙顶'
    )]
    for i in range(100):
        users.append(User(
            phone=f'176{i}',
            name=f'田所浩{i}',
            password='pbkdf2:sha256:260000$aDGiF8hQNDkHWtzz$80f75b5c1f286bba110476de4b75fe63e557720bf1805cb443881d2837ad4806',
            age=24,
            gender='男',
            email='114514@qq.com',
            address='东京下北泽'
        ))
    db.session.add_all(users)
    db.session.commit()
    # db = get_db()
    # with current_app.open_resource('schema.sql') as f:
    #     db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """自定义一个命令，用于初始化数据库，可在命令行键入以执行。
    Clear the existing data and create new tables.
    """
    init_db()
    click.echo('Initialized the database.')


def close_all_db(e=None):
    # db = g.pop('db', None)
    # if db is not None:
    #     db.close()
    g.pop('graph_db', None)
