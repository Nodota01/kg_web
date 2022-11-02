from html import escape
from webbrowser import get
from flask import Flask
from flask import render_template
from flask import request
from Result import *
from flask import session, g
import py2neo as neo
import db
import logging

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE='bolt://localhost:7687,neo4j,AAA200010199'
)
# app.teardown_appcontext()告诉 Flask 在返回响应后进行清理时调用该函数。
app.teardown_appcontext(db.close_db)
logging.basicConfig(level=logging.INFO)


@app.route('/')
def index_page():
    return render_template('index.html')


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
    param = request.json
    pattern = f'.*?{param["key_word"]}.*?'
    prop = prop_map[param['type']][param['prop']] if prop_map.get(
        param['type'], None) is not None and prop_map[param['type']].get(param['prop'], None) is not None else param['prop']
    result = Result({"categories": list(),
                     "nodes": list(),
                     "edges": list()})
    categories = set()
    g = db.get_db()
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
        result['nodes'].append(d)
    for relation in sub_g.relationships:
        e = dict()
        e['source'] = relation.start_node['uuid']
        e['target'] = relation.end_node['uuid']
        des_dict = dict(relation)
        des_dict.pop('uuid', None)
        e['des'] = type(relation).__name__ + (str(des_dict) if len(des_dict) != 0 else '')
        result['edges'].append(e)
    for c in categories:
        result['categories'].append({'name': c})
    logging.info(f'/q post val:{request.json}')
    return result.success()


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