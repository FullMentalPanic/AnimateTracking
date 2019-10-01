## -*- coding: utf-8 -*-
# Get every seasoned animate list
import scrapy
from animatetracking.items import *
import re
import logging

date_dict ={
    '一': '01',
    '四': '04',
    '七': '07',
    '十': '10',
}

class animatetracking(scrapy.Spider):
    name = "animatetracking"
    start_urls = [
        'https://www.acgmh.com/category/bangumi-lists',
    ]

    def parse(self, response):
        for item in self.animateseason(response):
            yield scrapy.Request(item['link'], callback=self.animatelist)

    def animateseason(self,response):
        for resource in response.xpath("//div[@class='post-info pos-r pd10 post-side']/h2[@class='entry-title']"):           
            item = AnimatetrackingItem()
            item['link'] = resource.css('a::attr(href)').extract()[0]
            date = resource.css('a *::text').extract()[0]
            item['date'] = '01-'+ date_dict[date[5]]+'-'+date[0:4] 
            yield item

    
    def animatelist(self,response):
        for resource in response.xpath("//h2/strong"):
            item = AnimatelistItem()
            item['animatetitle'] = resource.xpath('span/text()').extract_first()
            item['introducation'] = resource.xpath("../following-sibling::ul[1]/li[2]/text()").extract_first()
            yield item

