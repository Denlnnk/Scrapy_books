import scrapy
from scrapy import Request


def product_info(response, value: str):
    return response.xpath(f'//th[text()="{value}"]/following-sibling::td/text()').get()


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
        title = response.css('div.col-sm-6.product_main h1::text').get()
        price = response.css('p.price_color::text').get()
        description = response.xpath('//*[@id="product_description"]/following-sibling::p/text()').get()

        image_url = response.css('div.item.active img::attr(src)').get()
        image_url = self.start_urls[0] + image_url.replace('../../', '')

        rating = response.css('p.star-rating::attr(class)').get()
        rating = rating.replace('star-rating ', '')

        # product information
        upc = product_info(response, 'UPC')
        product_type = product_info(response, 'Product Type')
        price_before = product_info(response, 'Price (excl. tax)')
        price_after = product_info(response, 'Price (incl. tax)')
        tax = product_info(response, 'Tax')
        availability = product_info(response, 'Availability')
        number_of_reviews = product_info(response, 'Number of reviews')

        yield {
            'title': title,
            'price': price,
            'description': description,
            'image_url': image_url,
            'rating': rating,
            'upc': upc,
            'product_type': product_type,
            'price_before': price_before,
            'price_after': price_after,
            'tax': tax,
            'availability': availability,
            'number_of_reviews': number_of_reviews
        }
