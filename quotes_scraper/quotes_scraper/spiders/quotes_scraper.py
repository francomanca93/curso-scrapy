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

    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            quotes = kwargs['quotes']
        quotes_path = '//span[@class="text" and @itemprop="text"]/text()'
        quotes.extend(response.xpath(quotes_path).getall())
        
        next_page_button_path = '//ul[@class="pager"]//li[@class="next"]/a/@href'
        next_page_button_link = response.xpath(next_page_button_path).get()
        if next_page_button_link:
            yield response.follow(
                next_page_button_link, 
                callback=self.parse_only_quotes, 
                cb_kwargs={'quotes':quotes}
            )
        else:
            yield {
                'quotes': quotes
            }

    def parse(self, response):
        """ it help us to analize the file and extract information from this"""
        
        title_path = '//h1/a/text()'
        title = response.xpath(title_path).get()

        quotes_path = '//span[@class="text" and @itemprop="text"]/text()'
        quotes = response.xpath(quotes_path).getall()

        top_tags_path = '//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()'
        top_tags = response.xpath(top_tags_path).getall()
        
        top = getattr(self, 'top', None)
        if top:
            top = int(top)
            top_tags = top_tags[:top]

        yield {
            'title': title,
            'top_tags': top_tags
        }
        
        next_page_button_path = '//ul[@class="pager"]//li[@class="next"]/a/@href'
        next_page_button_link = response.xpath(next_page_button_path).get()
        if next_page_button_link:
            yield response.follow(
                next_page_button_link, 
                callback=self.parse_only_quotes, 
                cb_kwargs={'quotes': quotes}
            )
