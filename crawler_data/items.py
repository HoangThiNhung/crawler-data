# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_asin = scrapy.Field()
    product_name = scrapy.Field()
    product_is_have_patten = scrapy.Field()
    product_description = scrapy.Field()
    imported_code = scrapy.Field()
    image_link = scrapy.Field()
    original_image = scrapy.Field()
    color = scrapy.Field()
    price = scrapy.Field()
    patten = scrapy.Field()
    # link = scrapy.Field()
    # size = scrapy.Field()
