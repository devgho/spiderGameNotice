from ctypes.wintypes import DWORD
import scrapy
from gamenotice.items import GamenoticeItem


class YsSpider(scrapy.Spider):
    name = 'ys'
    allowed_domains = ['ys.mihoyo.com']
    start_urls = ['https://ys.mihoyo.com/main/news/12']

    def parse(self, response):
        a = response.xpath('//*[@id="frame"]/div[4]/div/div/ul[3]/li/a[contains(string(),"更新")]')
        if a.get():
            item = GamenoticeItem()
            item['url'] = response.urljoin(a.xpath('@href').get())
            item['title'] = a.xpath('div/h3/text()').get()
            item['dtime'] = a.xpath('following-sibling::div/div/text()').get()
            item['detail'] = "奇奇怪怪"
            yield item
        