from datetime import datetime
import scrapy,re,json
from gamenotice.items import GamenoticeItem


class YsSpider(scrapy.Spider):
    name = 'ys'
    allowed_domains = ['ys.mihoyo.com']
    start_urls = ['https://ys.mihoyo.com/main/news/12']
    

    def parse(self, response):
        serial_list = re.finditer('"\d{5}"', response.text)
        for i in serial_list:
            yield scrapy.Request("https://ys.mihoyo.com/content/ysCn/getContent?contentId="+i.group().replace('\"','')+"&around=1",callback=self.detail_parse)
        

    def detail_parse(self, response):
        rs = json.loads(response.text)
        if rs["message"] == "操作成功" and (("更新通知" or "维护通知") in rs['data']['title']):
            item = GamenoticeItem()
            item['title'] = rs["data"]['title']
            item['url'] = "https://ys.mihoyo.com/main/news/detail/"+rs['data']['contentId']
            item['dtime'] = rs['data']['start_time']
            item['detail'] = re.search(r"更新时间.*?。",re.sub(r'<.*?>',"",rs['data']['content']),re.S).group()
            return item