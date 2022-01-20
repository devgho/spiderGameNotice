from telnetlib import GA
import scrapy
import json
from gamenotice.items import GamenoticeItem
import time
import re


class SgzSpider(scrapy.Spider):
    name = 'sgz'
    allowed_domains = ['taptap.com']
    start_urls = ['https://www.taptap.com/webapiv2/apk/v1/list-by-app?app_id=139546&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D59%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3D807d4770-751d-49c0-b49a-6ea259fecd72%26DT%3DPC']

    def parse(self, response):
        rs = json.loads(response.text)
        if rs['success'] == True:
            newest = rs['data']['list'][0]
            item = GamenoticeItem()
            item['url'] = "https://www.taptap.com/app/139546/"
            item['title'] = newest['version_label']
            item['detail'] = re.sub("<.*?>","",newest['whatsnew']['text'])
            timeArray = time.localtime(newest['update_date'])
            item['dtime'] = time.strftime("%Y-%m-%d %H:%M:%S",timeArray)
            yield item