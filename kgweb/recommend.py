from flask import (Blueprint, current_app, render_template)
import pandas as pd
import os

bp = Blueprint('recommend', __name__)

@bp.get('/recommend')
def recommend():
    sheet = ['env', 'sport', 'behave', 'mental', 'food', 'soup', 'medic']
    sheet_name = ['环境建议', '运动建议', '习惯保持','心理建议','食谱建议','汤谱建议','药方建议']
    # 打开文件
    exs = [pd.read_excel(os.path.join(current_app.root_path, 'static/data/sleep_recommend.xlsx'), i).values.tolist() for i in range(len(sheet))]
    return render_template('recommend.html.j2', data = {item[0]:item[1] for item in zip(sheet, exs)}, sheet_name = list(zip(sheet, sheet_name)))