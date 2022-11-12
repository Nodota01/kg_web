from flask import current_app, g
import py2neo as neo
import sqlite3
import click

"""
该文件封装了所有数据库的连接
g是一个特殊对象，对于每个请求都是唯一的。它用于存储在请求期间可能被多个函数访问的数据。get_db如果在同一请求中第二次调用该连接，则该连接将被存储和重用，而不是创建新连接。
current_app是另一个特殊对象，它指向处理请求的 Flask 应用程序。由于您使用了应用程序工厂，因此在编写其余代码时没有应用程序对象。 get_db将在应用程序创建并正在处理请求时调用，因此current_app可以使用。
"""

def init_app(app):
    """注册会话结束后摧毁数据库连接，注册命令
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def get_graph_db():
    '''获取图数据库连接
    '''
    if 'graph_db' not in g:
        _res = current_app.config['GRAPH_DATABASE'].split(',')
        g.graph_db = neo.Graph(_res[0], auth=(_res[1], _res[2]))
    return g.graph_db

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    """初始化数据库，读取sql文件并执行
    """
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """自定义一个命令，用于初始化数据库，可在命令行键入以执行。
    Clear the existing data and create new tables.
    """
    init_db()
    click.echo('Initialized the database.')

def close_graph_db(e=None):
    graph_db = g.pop('graph_db', None)
    
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
