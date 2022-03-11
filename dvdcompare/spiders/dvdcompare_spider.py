import re
import scrapy


class DvdcompareSpiderSpider(scrapy.Spider):

    name = 'dvdcompare_spider'

    allowed_domains = ['dvdcompare.net']
    
    start_urls = ['http://dvdcompare.net/']

    def start_requests(self):
        return [
            scrapy.FormRequest(
                "https://dvdcompare.net/comparisons/search.php?param=Blu-ray&searchtype=text",
                method="POST",
                callback=self.extract_link_first
            )
            ]
    
    def extract_link_first(self,response):
        results = response.css('#content .col1-1>table ul a::attr(href)').getall()
        yield from response.follow_all(results,callback = self.extract_link)

    def extract_link(self,response):
        li = response.css('#content .col1-1>ul li')
        fi = filter(lambda x:'Blu-ray' in x.css('a::text').get(),li)
        yield from response.follow_all(map(lambda x:x.css('a::attr(href)').get(),fi),callback = self.parse)

    def parse(self, response):
        trs = response.css('#content>.col1-1 table tr')
        for i in trs:
            yield {
                'url':response.url,
                'content':self.delete_join(i.css('.dvd *::text').getall()),
                'amazon_url':i.css('iframe::attr(src)').get()
                }

    def delete_join(self,arr):
        de = map(lambda x:re.sub("[\r\n\t]","",x),arr)
        fi = filter(lambda y:y != '',de)
        delimiter = " "
        return delimiter.join(fi)
