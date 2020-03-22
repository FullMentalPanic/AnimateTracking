## -*- coding: utf-8 -*-
# Get every seasoned animate list
import scrapy
from animatetracking.items import *
import re
import logging
import datetime
import time

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
        now = datetime.datetime.now()
        max_date = now + datetime.timedelta(weeks = 13)
        min_date = now - datetime.timedelta(weeks = 13)
        link_list = []
        for resource in response.xpath("//div[@class='post-info pos-r pd10 post-side']/h2[@class='entry-title']"):           
            item = AnimatetrackingItem()
            item['link'] = resource.css('a::attr(href)').extract()[0]
            item['title'] = resource.css('a *::text').extract()[0]
            date = item['title']
            item['date'] = date[0:4]+'-'+date_dict[date[5]]+'-01'
            date_time = datetime.datetime.strptime(item['date'], '%Y-%m-%d')
            if ((min_date <= date_time) and (date_time <= max_date)):
                link_list.append(item['link'])
                yield item
        for link in link_list:
            yield scrapy.Request(link, callback=self.animatelist)
   
    def animatelist(self,response):
        count = 0
        table = response.xpath("//h1[@ref='postTitle']/text()").extract_first()        
        for resource in response.xpath("//div[@id='content-innerText']/h2"):
            item = AnimatelistItem()
            item['table'] = table
            sel = resource.xpath('strong/span/text()')
            item['animatetitle'] = sel.extract_first()
            if item['animatetitle'] is None:
                sel = resource.xpath('span/strong/text()')
                item['animatetitle'] = sel.extract_first()
            item['introducation'] = resource.xpath("following-sibling::ul[1]/li[2]/text()").extract_first()
            nums = []
            if nums is []:
                item = ''
            else:
                item['nums'] = ''.join(str(num) for num in nums)
            yield item
            count = count + 1
        print ("This season total animate is ", count)


