import scrapy
from gamenotice.items import GamenoticeItem
from datetime import datetime


class HpyjSpider(scrapy.Spider):
    name = 'hpjy'
    allowed_domains = ['gp.qq.com']
    start_urls = ['https://gp.qq.com/gicp/news/685/0/4001/1.html','https://gp.qq.com/gicp/news/685/0/4001/2.html']

    def parse(self, response):
        a = response.xpath('//*[@id="wrap"]/div/ul/li/a[contains(string(),"更新")]')
        if a.get():
            item = GamenoticeItem()
            item['url'] = response.urljoin(a.xpath('@href').get())
            item['title']= a.xpath('text()').get()          
            dtime = str(a.xpath('../em[@class="fr"]/text()').get())
            item['dtime'] = str(datetime.strptime(dtime,"%Y-%m-%d %H:%M"))
            yield scrapy.Request(item['url'],callback=self.detail_parse,meta={"item":item})

        
    def detail_parse(self, response): 
        response.meta['item']['detail'] = ''.join(response.xpath('//div[@class="article-box"]/p[position()<3]/text()').getall())
        return response.meta['item']