import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/page/1/'
    ]

    def parse(self, response):
        """ it help us to analize the file and extract information from this"""
        
        title_path = '//h1/a/text()'
        title = response.xpath(title_path).get()

        quotes_path = '//span[@class="text" and @itemprop="text"]/text()'
        quotes = response.xpath(quotes_path).getall()

        top_ten_tags_path = '//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()'
        top_ten_tags = response.xpath(top_ten_tags_path).getall()

        yield {
            'title': title,
            'quotes': quotes,
            'top_ten_tags': top_ten_tags
        }