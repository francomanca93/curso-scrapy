import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/page/1/'
    ]

    def parse(self, response):
        """ it help us to analize the file and extract information from this"""
        print('*' * 10)
        print('\n\n\n')
        
        title_path = '//h1/a/text()'
        title = response.xpath(title_path).get()
        print(f"Titulo: {title}")
        print('\n')

        quotes_path = '//span[@class="text" and @itemprop="text"]/text()'
        quotes = response.xpath(quotes_path).getall()
        print(f"Quotes")
        for quote in quotes:
            print(f"- {quote}")
        print('\n')

        top_ten_tags_path = '//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()'
        top_ten_tags = response.xpath(top_ten_tags_path).getall()
        print(f"Tags")
        for tag in top_ten_tags:
            print(f"- {tag}")
        print('\n')
        
        #print(response.status, response.headers)
        print('\n\n\n')
        print('*' * 10)
