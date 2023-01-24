import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/page/1/'
    ]

    def parse(self, response):
        """ it help us to analize the file and extract information from this"""
        print('*' * 10)
        print('\n\n')
        print(response.status, response.headers)
        print('*' * 10)
        print('\n\n')