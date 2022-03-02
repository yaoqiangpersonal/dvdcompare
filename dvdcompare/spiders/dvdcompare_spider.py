import re
import scrapy


class DvdcompareSpiderSpider(scrapy.Spider):

    name = 'dvdcompare_spider'

    allowed_domains = ['dvdcompare.net']
    
    start_urls = ['http://dvdcompare.net/']

    def start_requests(self):
        return [scrapy.FormRequest(
            "https://dvdcompare.net/comparisons/search.php?param=4K&searchtype=text",
            method="POST",
            callback=self.extract_link
            )]

    def extract_link(self,response):
        results = response.css('#content .col1-1>ul li a::attr(href)').getall()
        yield from response.follow_all(results,callback = self.parse)

    def parse(self, response):
        trs = response.css('#content>.col1-1 table tr')
        asin = response.css('#content>.col1-1 table .dvd')
        for i in trs:
            yield {'url':response.url,'content':self.delete_join(i.css('.dvd div::text').getall()),'amazon_url':i.css('iframe::attr(src)').get()}

    def delete_join(self,arr):
        de = map(lambda x:re.sub("[\r\n\t]","",x),arr)
        fi = filter(lambda y:y != '',de)
        delimiter = " "
        return delimiter.join(fi)
