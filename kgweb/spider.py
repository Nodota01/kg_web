'''
爬取 https://bjos.cn/list.html 上的恶意ip
'''
import redis
import datetime
import requests
from . import db
from bs4 import BeautifulSoup
header = {
"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"accept-encoding": "gzip, deflate, br",
"accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
"cache-control": "max-age=0",
"referer": "https://bjos.cn/cha.html",
"sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
"sec-ch-ua-mobile": "?0",
"sec-ch-ua-platform": "Windows",
"sec-fetch-dest": "document",
"sec-fetch-mode": "navigate",
"sec-fetch-site": "same-origin",
"sec-fetch-user": "?1",
"upgrade-insecure-requests": '1',
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54"
}
base_url = 'https://bjos.cn'

#用redis做个缓存
def get_badip()->list:
    key_name = 'badip'
    r = db.get_redis_db()
    if r is not None and r.exists(key_name): 
        return r.lrange(key_name,0, -1)
    else:
        try:
            with requests.Session() as session:
                main_page = BeautifulSoup(session.get(url=base_url+'/list.html', headers=header, timeout=5).text, 'html.parser')
                detail_page_url = base_url + main_page.select('center>a')[1].get('href')
                detail_page = BeautifulSoup(session.get(url=detail_page_url, headers=header, timeout=5).text, 'html.parser')
                res =  list(map(lambda item : item.string, detail_page.select('center>a')))
                if r is not None:
                    for ip in res : r.rpush(key_name,ip)
                    r.expire(key_name, datetime.timedelta(days=1))
                return res
        except requests.ConnectionError as e:
            print(e)
            return list()