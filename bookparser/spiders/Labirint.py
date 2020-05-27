# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem

class LabirintSpider(scrapy.Spider):
    name = 'Labirint'
    allowed_domains = ['labirint.ru']
    # start_urls = ['https://www.labirint.ru/search/python/?stype=0']


    def __init__(self, name_branch):
        self.start_urls = [f'https://www.labirint.ru/search/{name_branch}/?stype=0']


    def parse(self, response:HtmlResponse):
        next_page = response.css('a.pagination-next__text::attr(href)').extract_first()
        books_link = response.css('a.cover::attr(href)').extract()
        for book_link in books_link:
            yield response.follow(book_link, callback=self.book_parse)
        yield response.follow(next_page, callback=self.parse)


    def book_parse(self, response:HtmlResponse):
        name = response.xpath("//div[@id='product-title']/h1/text()").extract()
        link = response.url
        authors = response.xpath("//div[@class='authors']/a/text()")[0].extract()
        rating = response.xpath("//div[@id='rate']/text()").extract()
        main_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").extract()
        discount_price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").extract()

        yield BookparserItem(name=name, authors=authors, link=link, rating=rating,main_price=main_price, discount_price=discount_price)