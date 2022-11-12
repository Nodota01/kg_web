class Result:
    """API返回模板，维护一个data字典，以及代码与信息
    """
    def __init__(self, data = dict()):
        self.__data = data
        self.__code = 0
        self.__msg = ''

    def __getitem__(self, key):
        return self.__data.get(key, None)
    
    def __setitem__(self, key, value):
        self.__data[key] = value
        
    def __delitem__(self, key):
        if key in self.__date: del self.__date[key]
        
    def empty(self) -> dict :
        return {'code':2, 'msg':'empty'}
        
    def success(self) -> dict :
        return {'code':1, 'msg':'success', 'data':self.__data}
    
    def fail(self) -> dict :
        return {'code':0, 'msg':'fail', 'data':''}