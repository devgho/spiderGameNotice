# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import requests
from itemadapter import ItemAdapter
import json,re
from datetime import datetime


class GamenoticePipeline:
    def open_spider(self,spider):
        self.file = open(f"notices/{spider.name}.json","a+",encoding="utf8")
        self.file.seek(0)
        old = self.file.read()
        old_json = json.loads(old if old != "" else '{"dtime":"2000-01-12 10:30:13"}')
        self.old_dtime = datetime.strptime(old_json['dtime'], "%Y-%m-%d %H:%M:%S")

    def process_item(self, item, spider):
        new_dtime = datetime.strptime(item['dtime'], "%Y-%m-%d %H:%M:%S")
        if self.old_dtime > new_dtime:
            pass
        elif self.old_dtime < new_dtime:
            url = "https://oapi.dingtalk.com/robot/send?access_token=3ce7a6e1c237c06473f9b0f8b226c2428f9ff4d02a5cf73584e38d07beafc23c"
            message = f"###  {item['title']}  \n  {item['dtime']}  \n \n {item['detail'][:50]}  \n  {item['url']}  \n  {spider.name}"""
            data = {
                "msgtype":"markdown",
                "markdown":{
                    "title":spider.name,
                    "text": message,
                }
            }
            requests.post(url,json=data)
            self.file.seek(0)
            self.file.truncate()
            v = json.dumps(dict(item),ensure_ascii=False)
            self.file.write(v)
        return item

    def close_spider(self,spider):
        self.file.close()