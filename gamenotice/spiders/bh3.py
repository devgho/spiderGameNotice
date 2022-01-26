import scrapy,re
from gamenotice.items import GamenoticeItem
from datetime import datetime


class Bh3Spider(scrapy.Spider):
    name = 'bh3'
    allowed_domains = ['www.bh3.com']
    start_urls = ['https://www.bh3.com/news/cate/171']

    def parse(self, response):
        new = response.xpath('//div[@class="news-list"]/div/a/div[@class="news-item__bd"]/div[@class="news-item__title"]/div[contains(string(),"更新") or contains(string(),"维护")]')
        if new.get():
            item = GamenoticeItem()
            item['title'] = new.xpath("text()").get()
            item['dtime'] = str(datetime.strptime(re.search(r'\d{4}-\d{1,2}-\d{1,2}',new.xpath("following-sibling::*").get()).group(),"%Y-%m-%d"))
            item['url'] = response.urljoin(new.xpath("../../../@href").get())
            return scrapy.Request(item['url'],callback=self.detail_parse,meta=item)

    
    def detail_parse(self, response):
        response.meta['detail'] = re.sub(r"<.*?>","",response.xpath("//div[@class='article__bd']").get())
        return response.meta