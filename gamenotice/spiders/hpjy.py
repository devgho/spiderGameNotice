import scrapy
from gamenotice.items import GamenoticeItem


class HpyjSpider(scrapy.Spider):
    name = 'hpjy'
    allowed_domains = ['gp.qq.com']
    start_urls = ['https://gp.qq.com/gicp/news/685/0/4001/1.html']

    def parse(self, response):
        a = response.xpath('//*[@id="wrap"]/div/ul/li/a[contains(string(),"更新")]')
        if a.get():
            item = GamenoticeItem()
            url = response.urljoin(a.xpath('@href').get())
            yield scrapy.Request(url)
            item['url'] = url
            item['title']= a.xpath('text()').get()                    
            item['dtime'] = a.xpath('../em[@class="fr"]/text()').get()
            yield item