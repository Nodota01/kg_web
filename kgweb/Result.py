class Result:
    """API返回模板，维护一个data字典，以及代码与信息
    """
    def __init__(self, data = dict(), page = None):
        self.__data = data
        if page is not None: # 如果有，读分页信息
            self.__data['items'] = page.items
            self.__data['page'] = page.page
            self.__data['per_page'] = page.per_page
            self.__data['total'] = page.total
            self.__data['first'] = page.first
            self.__data['last'] = page.last
            self.__data['pages'] = page.pages
            self.__data['has_prev'] = page.has_prev
            self.__data['has_next'] = page.has_next
            self.__data['prev_num'] = page.prev_num
            self.__data['next_num'] = page.next_num
            self.__data['iter_pages'] = list(page.iter_pages())

    def __getitem__(self, key):
        return self.__data.get(key, None)
    
    def __setitem__(self, key, value):
        self.__data[key] = value
        
    def __delitem__(self, key):
        if key in self.__date: del self.__date[key]
        
    def unauthorized(self) -> dict :
        return {'code':4, 'msg':'unauthorized'}
        
    def redirect(self, url : str) -> dict :
        return {'code':3, 'msg':'redirect', 'data':{'url':url}}
    
    def empty(self) -> dict :
        return {'code':2, 'msg':'empty'}
        
    def success(self) -> dict :
        return {'code':1, 'msg':'success', 'data':self.__data}
    
    def fail(self, error : str = None) -> dict :
        if str is not None:
            self.__data['error'] = error
        return {'code':0, 'msg':'fail', 'data':self.__data}