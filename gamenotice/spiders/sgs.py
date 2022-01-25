import scrapy,re
from gamenotice.items import GamenoticeItem


class SgsSpider(scrapy.Spider):
    name = 'sgs'
    allowed_domains = ['www.sanguosha.cn']
    start_urls = ['https://www.sanguosha.cn/news-list-1002.html']

    def parse(self, response):
        news_list = response.xpath('//*[@id="innerPress"]')
        if news_list.get():
            p = news_list.xpath('li/a/p[contains(string(),"更新") or contains(string(),"维护")]')
            if p.get():
                url = p.xpath('../@href').get()
                return scrapy.Request(url,callback=self.detail_parse)

    

    def detail_parse(self, response):
        item = GamenoticeItem()
        item['title'] = response.xpath('//div[@class="art-title"]/text()').get()
        item['url'] = response.url
        item['dtime'] = response.xpath('//p[@class="art-time"]/text()').get().replace("时间：","")
        item['detail'] = re.sub(r"<.*?>","",response.xpath('//div[@class="art-info"]').get())
        
        return item