# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class AnimatelistItem(scrapy.Item):
    # define the fields for your item here like:
    table = scrapy.Field()
    animatetitle = scrapy.Field()
    othertitle = scrapy.Field()
    nums = scrapy.Field()
    cross = scrapy.Field()
    last_title = scrapy.Field()

    pass