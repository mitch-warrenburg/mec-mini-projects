import scrapy


class CssQuotesScraper(scrapy.Spider):
    name = "toscrape-css"
    start_urls = ['https://quotes.toscrape.com/page/1/']

    def parse(self, response, **kwargs):
        for quote in response.css('div.quote'):
            yield {
                'author': quote.css('span small::text').get(),
                'text': quote.css('span.text::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


class XpathQuotesScraper(scrapy.Spider):
    name = "toscrape-xpath"
    start_urls = ['https://quotes.toscrape.com/page/1/']

    def parse(self, response, **kwargs):
        for quote in response.xpath('//div[@itemscope]'):
            yield {
                'author': quote.xpath('.//small/text()').get(),
                'text': quote.xpath('span[@itemprop="text"]/text()').get(),
                'tags': quote.xpath('./div//a/text()').getall(),
            }

        next_page = response.xpath('//li[@class="next"]/a/@href').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
