# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem

class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    # start_urls = ['https://book24.ru/search/?q=python']

    def __init__(self, name_branch):
        self.start_urls = [f'https://book24.ru/search/?q={name_branch}']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[@class='catalog-pagination__item _text js-pagination-catalog-item']/@href").extract_first()
        books_link = response.xpath("//a[@class='book__title-link js-item-element ddl_product_link ']/@href").extract()
        for book_link in books_link:
            yield response.follow(book_link, callback=self.book_parse)
        yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response:HtmlResponse):
        name = response.xpath("//div[@class='item-detail__informations-box']/h1/text()").extract()
        link = response.url
        authors = response.xpath("//a[@class='item-tab__chars-link js-data-link']/text()").extract()
        rating = [5]
        main_price = response.xpath("//div[@class='item-actions__price']/b/text()").extract()
        discount_price = main_price

        yield BookparserItem(name=name, authors=authors, link=link, rating=rating,main_price=main_price, discount_price=discount_price)