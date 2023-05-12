from flask import (Blueprint, current_app, render_template,
                   request)
from . import Result, model_assert

bp = Blueprint('herb_recommend', __name__)

@bp.route("/herb_recommend", methods = ['GET'])
def herb_recommend():
    return render_template('herb_recommend.html.j2', symptom_contain = model_assert.model_loader.symptom_contain_sorted)

@bp.route("/get_herbs", methods = ['POST'])
def get_herbs():
    '''
    返回推荐的草药以及其相似草药，形如
    {'A':['A, 'B']}
    '''
    current_app.logger.debug(request.json)
    if not request.is_json or not isinstance(request.json['symps'], list) :
        return Result().fail('data error')
    if len((set(request.json['symps']) & set(model_assert.model_loader.symptom_contain))) != len(request.json['symps']): # 症状不在支持的集合中
        return Result().fail('symps not contain!')
    try:
        return Result(model_assert.model_loader.get_recommend_herb(request.json['symps'],k = request.json['k'])).success()
    except Exception as e: # 模型异常
        return Result().fail(str(e) + 'model error')

@bp.route('/herb_contain', methods = ['GET'])
def herb_contain():
    return Result(model_assert.model_loader.herb_contain).success()

@bp.route('/symptom_contain', methods = ['GET'])
def symptom_contain():
    return Result(model_assert.model_loader.symptom_contain_sorted).success()
