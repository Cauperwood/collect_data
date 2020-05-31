# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

def clean_int(val_int):
    val_int = val_int.split()
    for i in range(len(val_int)):
        if val_int[i] == ' ':
            val_int.pop([i])
    return float(''.join(val_int))


def clean_str(val_str):
    val_str = ''.join(val_str).split()
    return val_str


class LeroymerlinparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    main_price = scrapy.Field(input_processor=MapCompose(clean_int))
    currency = scrapy.Field()
    unit = scrapy.Field()
    photos = scrapy.Field()
    link = scrapy.Field(output_processor=TakeFirst())
    name_characteristics = scrapy.Field()
    value_characteristics = scrapy.Field(input_processor=clean_str)

