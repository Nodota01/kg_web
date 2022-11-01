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
    diseases = request.json
    pattern = f'.*?{diseases["key_word"]}.*?'
    # for dis in diseases:
    #     pattern += f'.*?{dis[0:len(dis)-1]}.*?|'
    # pattern = pattern.rstrip('|')
    g = db.get_db()
    # node_matcher = neo.NodeMatcher(graph)
    # rela_matcher = neo.RelationshipMatcher(graph)
    # shiliao_nodes = node_matcher.match('食疗食谱', 主治=neo.LIKE(pattern))
    # nodes = list()
    # for node in shiliao_nodes.all():
    #     nodes.append(node)
    result = Result({"categories":list(),
           "nodes":list(),
           "edges":list()})
    categories = set()
    sub_g = g.run(f'MATCH (a:方剂)<-[r:材料]->(b) WHERE a.主治 =~ "{pattern}" return a, r, b').to_subgraph()
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
        d['name'] = n.get('中文名', None) if n.get('中文名', None) is not None else n.get('名称', None)
        result['nodes'].append(d)
    for relation in sub_g.relationships:
        e = dict()
        e['source'] = relation.start_node['uuid']
        e['target'] = relation.end_node['uuid']
        e['des'] = str(dict(relation))
        result['edges'].append(e)
    for c in categories:
        result['categories'].append({'name':c})
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
