import scrapy,re
from gamenotice.items import GamenoticeItem


class YsSpider(scrapy.Spider):
    name = 'ys'
    allowed_domains = ['ys.mihoyo.com']
    start_urls = ['https://ys.mihoyo.com/main/news/12']

    def parse(self, response):
        serial_list = re.finditer('"\d{5}"', response.text)
        # for i in serial_list:
        with open("1.txt","a+") as f:
            f.write(serial_list)
        
    def detail_parse(self, response):
        pass