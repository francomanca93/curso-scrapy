import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/page/1/'
    ]
    custom_settings = {
        'FEEDS': {
            'quotes.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'fields': None,
                'indent': 4,
                'item_export_kwargs': {
                    'export_empty_fields': True,
                },
            },
        },
    }

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
        
        next_page_button_path = '//ul[@class="pager"]//li[@class="next"]/a/@href'
        next_page_button_link = response.xpath(next_page_button_path).get()
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse)
