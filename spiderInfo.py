import requests
from requests.exceptions import RequestException
from urllib.parse import urlencode
from pyquery import PyQuery as pq
import pymongo
from config import *
import log

class SpiderInfo():
    
    def __init__(self):
        # 连接mongodb
        self._client = pymongo.MongoClient(MONGO_URL)
        self._db = self._client[MONGO_DB]

        # 初始化日志记录
        self._logger=log.logs()

        # 请求连接
        self._base_url = 'http://www.6vhao.tv/'
        self._base_header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400'
        }

    # 获取首页数据
    def get_index(self):
        try:
            response = requests.get(self._base_url)    
            response.encoding = 'GBK'
            if response.status_code == 200:
                return response.text
            else:
                self._logger.error('连接到v6电影网出现异常！')
            return None
        except RequestException:
            self._logger.error('连接到v6电影网出现异常！')

    # 解析首页数据
    def parse_index(self):
        index_result = self.get_index()
        # 解析获取（电影电视剧分类）
        doc = pq(index_result)
        # 电影分类
        movie_tpye_items = doc('.channeltype').items()
        for item in movie_tpye_items:
            # 分类名
            movie_tpye_name = item('h2 > a').text()
            # 分类链接
            movie_tpye_link = item('h2 > a').attr('href')
            print(movie_tpye_name, movie_tpye_link)
            # 该分类火爆电影电视剧

    def run(self):
        self.parse_index()


    