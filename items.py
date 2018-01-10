# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import datetime
import scrapy


class CoinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    histdate = scrapy.Field(default=datetime.date.today())
    name = scrapy.Field()
    symbol = scrapy.Field()
    market = scrapy.Field()
    price = scrapy.Field()
    supply = scrapy.Field()
    volume = scrapy.Field()
