import scrapy 

from scrapy_splash import SplashRequest

class ebaySpider(scrapy.Spider):
    name='ebay'

    def start_requests(self):
        yield SplashRequest(url='https://www.ebay.com/b/Apple-iPhone/9355/bn_319682', callback=self.parse, endpoint='render.html', args={'wait': 0.5}, dont_filter=True)


    def parse(self, response):
        for item in response.xpath("//li[@class='s-item']"):
            yield {
                'product': item.xpath(".//h3[@class='s-item__title']/text()").extract_first(),
                "price": item.xpath(".//span[@class='s-item__price']/text()").extract_first()
            }
        
        next_page = response.xpath("//a[@rel='next']/@href").extract_first()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield SplashRequest(url=next_page, callback=self.parse, endpoint='render.html', args={'wait': 1}, dont_filter=True)


    