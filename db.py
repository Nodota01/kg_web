from flask import current_app, g
import py2neo as neo

def get_db():
    '''
    g是一个特殊对象，对于每个请求都是唯一的。它用于存储在请求期间可能被多个函数访问的数据。get_db如果在同一请求中第二次调用该连接，则该连接将被存储和重用，而不是创建新连接。
    current_app是另一个特殊对象，它指向处理请求的 Flask 应用程序。由于您使用了应用程序工厂，因此在编写其余代码时没有应用程序对象。 get_db将在应用程序创建并正在处理请求时调用，因此current_app可以使用。
    '''
    if 'db' not in g:
        _res = current_app.config['DATABASE'].split(',')
        g.db = neo.Graph(_res[0], auth=(_res[1], _res[2]))
    return g.db

def close_db(e=None):
    db = g.pop('db', None)