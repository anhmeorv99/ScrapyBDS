# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VnexpressItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    phone_number = scrapy.Field()

    name_apartment = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    address_apartment = scrapy.Field()
    pass
