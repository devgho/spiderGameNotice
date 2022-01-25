# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import requests
from itemadapter import ItemAdapter
import json
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
            url = "https://oapi.dingtalk.com/robot/send?access_token=45e040c0bd4ece2dbee76e714cfde47655bd2628dc58ed93697e57eedbaf3f43"
            message = f"### {spider.name}更新啦 时间:{item['dtime']} \n > {item['detail'][:70]}...  [点击查看详情]({item['url']})"""
            data = {
                "msgtype":"markdown",
                "markdown":{
                    "title":spider.name+"更新啦",
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