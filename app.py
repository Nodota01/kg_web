from html import escape
from flask import Flask
from flask import render_template
from flask import request
from flask import session, g
import py2neo as neo
import json
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
    graph = db.get_db()
    node_matcher = neo.NodeMatcher(graph)
    rela_matcher = neo.RelationshipMatcher(graph)
    shiliao_nodes = node_matcher.match('食疗食谱', 主治=neo.LIKE(pattern))
    nodes = list()
    for node in shiliao_nodes.all():
        nodes.append(node)
    logging.info(f'/q post val:{request.json} res:{len(nodes)}')
    return nodes
    


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
