## -*- coding: utf-8 -*-
# Get every seasoned animate list
import scrapy
from animatetracking.items import *
import re


class animatelistspider(scrapy.Spider):
    name = "dmhy_rss"
    start_urls = [
        'https://justlaughtw.blogspot.com/search/label/%E6%96%B0%E7%95%AA%E5%88%97%E8%A1%A8?max-results=6',
    ]

    def parse(self, response):
        for item in self.animateseason(response):
            yield item

    def animateseason(self,response):
        for response in response.xpath("")