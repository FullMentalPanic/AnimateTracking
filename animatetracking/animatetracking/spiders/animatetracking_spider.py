## -*- coding: utf-8 -*-
# Get every seasoned animate list
import scrapy
from animatetracking.items import *
import re
import logging
import datetime
import time
import re 
from zhon.hanzi import punctuation
import string

import pymysql

class animatetracking(scrapy.Spider):
    name = "animatetracking"
    start_urls = [
        'https://acgsecrets.hk/bangumi/202101/',
    ]
    def __init__(self):
        self.name = "animatetracking"
        now = datetime.datetime.now()
        temp = str(now.year)
        if now.month < 4:
            self.playlist = temp + '01'
        elif now.month < 7:
            self.playlist = temp + '04'
        elif now.month < 10:
            self.playlist = temp + '07'
        elif now.month <= 12:
            self.playlist = temp + '10'
        
        self.start_urls = [
            'https://acgsecrets.hk/bangumi/' + self.playlist + '/',
        ]

    def parse(self, response):
        #self.updateSQLtable()
        animatelist = response.xpath("//div[@id='acgs-anime-list']")
        for resource in animatelist.xpath("//div[@acgs-bangumi-anime-id]"):
            item = AnimatelistItem()
            animatetitle = resource.xpath(".//h3[@class='entity_localized_name']/text()").extract_first()
            item['table'] = 's'+self.playlist
            item['animatetitle'] = self.remove_punctuation(animatetitle)
            othertitle = resource.xpath(".//div[@class='anime_summary']/i/text()").extract_first()
            cross = resource.xpath(".//div[@class='anime_onair time_today']/text()").extract_first()
            value = 'N'
            if cross:
                if "跨" in cross:
                    value = 'Y'
            
            item['cross'] = value
            item['nums']= '1'
            item['last_title'] = ''
            if othertitle:
                othertitle = othertitle[5:]
            else:
                othertitle = ''
            item['othertitle'] = self.split_punctuation(othertitle)
            yield item

    def split_punctuation(self,line):
        punctuation = """、"""
        re_punctuation = "[{}]+".format(punctuation)
        line = re.sub(re_punctuation,",", line)
        tiles = line.split(",")
        result = ''

        for tile in tiles:
            result = result + self.remove_punctuation(tile) +','
        
        return result[0:-1]

    def remove_punctuation(self, line, strip_all=True):
        if strip_all:
            rule = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]")
            line = rule.sub(' ',line)
        else:
            punctuation = """！？｡＂＃＄％＆＇（）＊＋－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏"""
            re_punctuation = "[{}]+".format(punctuation)
            line = re.sub(re_punctuation," ", line)

        return line.strip()




