# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AnimatetrackingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    pass
class AnimatelistItem(scrapy.Item):
    # define the fields for your item here like:
    table = scrapy.Field()
    animatetitle = scrapy.Field()
    introducation = scrapy.Field()
    nums = scrapy.Field()
    last_title = scrapy.Field()
    pass