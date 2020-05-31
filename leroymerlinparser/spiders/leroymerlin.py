# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from leroymerlinparser.items import LeroymerlinparserItem
from scrapy.loader import ItemLoader


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']
    # https://leroymerlin.ru/search/?q=%D0%BE%D0%B1%D0%BE%D0%B8%2F&tab=products&sortby=8&page=1
    def __init__(self, name_branch):
        # self.start_urls = [f'https://leroymerlin.ru/search/?q={name_branch}%2F&tab=products&sortby=8&page=1']
        self.start_urls = [f'https://leroymerlin.ru/search/?q={name_branch}']

    def parse(self, response:HtmlResponse):
        # next_page = response.css('a.next-paginator-button::attr(href)').extract_first()
        s = 'https://leroymerlin.ru'
        next_page = response.xpath("//div[@class='next-paginator-button-wrapper']/a[@class='paginator-button next-paginator-button']/@href").extract_first()
        goods_link = response.xpath("//a[@class='black-link product-name-inner']/@href").extract()
        for good_link in goods_link:
            yield response.follow(s + good_link, callback=self.good_parse)
        yield response.follow(s + next_page, callback=self.parse)


    def good_parse(self,response:HtmlResponse):
        loader = ItemLoader(item=LeroymerlinparserItem(), response=response)
        loader.add_xpath('name', "//h1[@slot='title']/text()")
        loader.add_value('link', response.url)
        loader.add_xpath('main_price', "//span[@slot='price']/text()")
        loader.add_xpath('currency', "//span[@slot='currency']/text()")
        loader.add_xpath('unit', "//span[@slot='unit']/text()")
        loader.add_xpath('photos', "//source[@media=' only screen and (min-width: 1024px)']/@data-origin")
        loader.add_xpath('name_characteristics', "//dt[@class='def-list__term']/text()")
        loader.add_xpath('value_characteristics', "//dd[@class='def-list__definition']/text()")
        # name = response.xpath("//h1[@slot='title']/text()").extract()
        # link = response.url
        # main_price = response.xpath("//span[@slot='price']/text()").extract()
        # currency = response.xpath("//span[@slot='currency']/text()").extract()
        # unit = response.xpath("//span[@slot='unit']/text()").extract()
        # photos = response.xpath("//source[@media=' only screen and (min-width: 1024px)']/@data-origin").extract()
        # rating = [5]
        # main_price = response.xpath("//div[@class='item-actions__price']/b/text()").extract()
        # discount_price = main_price
        yield loader.load_item()

