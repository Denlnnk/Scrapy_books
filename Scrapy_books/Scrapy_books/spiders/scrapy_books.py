import scrapy
from scrapy import Request


class ScrapyBooksSpider(scrapy.Spider):
    name = 'scrapy_books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response, **kwargs):
        for book_url in response.css('h3 a::attr(href)').getall():
            absolute_book_url = response.urljoin(book_url)
            yield Request(absolute_book_url, callback=self.parse_book)

        next_page_url = response.css('li.next a::attr(href)').get()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield Request(absolute_next_page_url)

    def parse_book(self, response):
        pass
