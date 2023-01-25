import scrapy
import lxml.html as html


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
        'CONCURRENT_REQUESTS': 24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['fm@fm.com'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': ''
    }

    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            # Generate new Quotes (Page)
            new_quotes = self._get_all_quotes_information(response)
            kwargs["quotes"].extend(new_quotes)
            # Get the new link
            next_page = self._get_next_link(response)
            if next_page:
                yield response.follow(
                    next_page,
                    callback=self.parse_only_quotes,
                    cb_kwargs=kwargs
                )
            else:
                yield kwargs

    def parse(self, response):
        """ it help us to analize the file and extract information from this"""
        title = self._get_title(response)
        quotes = self._get_all_quotes_information(response)
        top_tags = self._get_top_tags(response)

        # Get the new link
        next_page = self._get_next_link(response)
        if next_page:
            yield response.follow(
                next_page,
                callback=self.parse_only_quotes,
                cb_kwargs={
                    "title": title, 
                    "top_tags": top_tags,
                    "quotes": quotes
                }
        )

    # Basic data private methods
    def _get_title(self, response):
        return response.xpath('//h1/a/text()').get()

    def _get_all_quotes_information(self, response):
        quotes = self.__get_all_quotes(response)
        authors = self.__get_all_author(response)
        tags = self.__get_quote_tags(response)
        return [({'quote': one, 'author': two, 'tags': three}) for one, two, three in zip(quotes, authors, tags)]

    def __get_all_quotes(self, response):
            return response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()

    def __get_all_author(self, response):
        return response.xpath('//span/small[@class="author" and @itemprop="author"]/text()').getall()

    def __get_quote_tags(self, response):
        tag_path = '//div[contains(@class, "quote")]//div[contains(@class, "tags")]'
        tags_html_in_list = response.xpath(tag_path).getall()
        
        tags = []
        for tag_html in tags_html_in_list:
            tag_parsed = html.fromstring(tag_html)
            every_tag_path = '//a[@class="tag"]/text()'
            quote_tags = tag_parsed.xpath(every_tag_path)
            tags.append(quote_tags)
        
        return tags

    def _get_top_tags(self, response):
        ''' Generate Content -a [OPTION]\nOption: -a top=3 Get the first 3 of the top '''
        top_tags = response.xpath('//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()
        # Add Params
        top = getattr(self, 'top', None)
        if top:
            top_tags = top_tags[:int(top)]
        return top_tags

    # Get the new link private method
    def _get_next_link(self, response):
        return response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
