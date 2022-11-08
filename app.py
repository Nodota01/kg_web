from html import escape
from webbrowser import get
from flask import Flask
from flask import render_template
from flask import request
from Result import *
from flask import session, g
from flask import send_from_directory
import os
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

@app.route('/favicon.ico')#设置icon
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),#对于当前文件所在路径,比如这里是static下的favicon.ico
                               'favicon.ico', mimetype='type="image/x-icon"')

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
