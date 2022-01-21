import scrapy
import json,re
from gamenotice.items import GamenoticeItem


class SgzSpider(scrapy.Spider):
    name = 'sgz'
    allowed_domains = ['sgzzlb.lingxigames.com','sapi.aligames.com']
    
    def start_requests(self):
        url = "https://sapi.aligames.com/ds/ajax/endpoint.json"
        data = {"api":"/api/l/owresource/getListRecommend","params":{"gameId":10000100,"collectionIds":"129,143,128,736,142,194","orderCode":1,"orderDesc": True,"page":0,"size":20}}
        yield scrapy.FormRequest(url, method="POST", body=json.dumps(data), headers={'Content-Type': 'application/json'},callback=self.parse)

    def parse(self, response):
        rs = json.loads(response.text)
        if bool(rs['success']) == True:
            rlist = rs['result']['list']
            for i in rlist:
                if "维护" in i['title'] or "更新" in i['title']:
                    item = GamenoticeItem()
                    item['title'] = i['title']
                    item['url'] = "https://sgzzlb.lingxigames.com/news/article/?id="+str(i['id'])
                    item['dtime'] = i['mtime']
                    data = {"api": "/api/l/owresource/getInfoDetail", "params": {"gameId": i['gameId'], "id": i['id']}}
                    return scrapy.FormRequest(response.url, method="POST", headers={"Content-Type":"application/json"} ,body=json.dumps(data), callback=self.detail_parse, meta=item)
    
    def detail_parse(self, response):
        rs = json.loads(response.text)
        if bool(rs['success'] == True):
            response.meta['detail'] = re.sub("<.*?>","",rs['result']['content'])
            return response.meta