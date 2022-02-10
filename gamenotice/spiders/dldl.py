from array import array
import json,re
import scrapy
from gamenotice.items import GamenoticeItem


class DldlSpider(scrapy.Spider):
    name = 'dldl'
    allowed_domains = ['hsdj.37.com.cn']
    start_urls = ['https://mg-api.37.com.cn/website/articlelist/51/95?webId=51&categoryId=95&pageSize=8&pageNum=1']

    def parse(self, response):
        rs = json.loads(response.text)
        for i in rs['data']['array'][:2]:
            if ("版本更新说明" or "维护" or "停机") in i['title']:
                item = GamenoticeItem()
                item['title'] = i['title']
                item['url'] = "https://hsdj.37.com.cn/article/"+str(i['articleId'])
                item['dtime'] = i['time']
                item['detail'] = re.search(r"更新时间#.{1,30}",re.sub(r'<.*?>',"",i['content'])).group()
                yield item