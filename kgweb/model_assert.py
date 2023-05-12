# 静态类，加载模型数据
import torch
import os
import json


class ModelLoader():
    def __init__(self, app):
        app.logger.debug('loading models.....')
        with open(os.path.join(app.root_path, 'static/data/herbs_contains.txt'), 'r', encoding='utf8') as f_herbs_contains, open(os.path.join(app.root_path, 'static/data/symptom_contains.txt'), 'r', encoding='utf8') as f_symptom_contains, open(os.path.join(app.root_path, 'static/data/symptom_contains_sorted.txt'), 'r', encoding='utf8') as f_symptom_contains_sorted:
            self.herb_contain = [h.strip('\n')
                                 for h in f_herbs_contains.readlines()]
            self.symptom_contain = [s.strip('\n')
                                    for s in f_symptom_contains.readlines()]
            self.symptom_contain_sorted = [
                s.strip('\n') for s in f_symptom_contains_sorted.readlines()]
        self.__mlp_model : torch.nn.Module = torch.load(os.path.join(
            app.root_path, 'static/data/model/MLP.pth'), map_location=torch.device('cpu')).train(False)
        # self.trans_model : models.ERModel = torch.load(os.path.join(app.root_path, 'static/data/model/TransE_50.pkl'), map_location=torch.device('cpu'))
        self.__simi_dict = json.load(open(os.path.join(
            app.root_path, 'static/data/TransE50_simi_herbs.json'), mode='r', encoding='utf8'))
        app.logger.debug('loading models.....done')

    def get_recommend_herb(self, symps: list[str], k: int = 5) -> dict[str, list]:
        '''
        获取k个推荐的草药，以及10个相似草药
        '''
        symps_ids = [self.symptom_contain.index(h) for h in symps]
        symps_multi_hot = torch.zeros((1, 390), dtype=torch.int32)
        for index in symps_ids:
            symps_multi_hot[0][index] = 1
        herbs_ids = torch.topk(self.__mlp_model(
            symps_multi_hot.float())[0], k)[1]
        herbs = [self.herb_contain[h] for h in herbs_ids]
        return {h: self.__simi_dict[h][:10] for h in herbs}


model_loader = None


def load_model(app):
    global model_loader
    if model_loader is not None:
        pass
    model_loader = ModelLoader(app)
