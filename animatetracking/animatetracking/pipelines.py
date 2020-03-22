# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from scrapy.exceptions import NotConfigured
from animatetracking.items import AnimatetrackingItem,AnimatelistItem
from animatetracking import settings


class AnimatetrackingPipeline(object):

    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if isinstance(item,AnimatetrackingItem):
            sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = \'" + item["title"] +"\'"
            
            self.cursor.execute(sql)
            if self.cursor.fetchone()[0] == 0:
                sql = "CREATE TABLE " +str(item["title"]) + " (animatetitle text, introducation text, nums text)"
                self.cursor.execute(sql)



        if isinstance(item,AnimatelistItem):
            sql = """select * from {} where animatetitle = \'{}\'""".format(item["table"],item["animatetitle"])
            self.cursor.execute(sql)
            if not self.cursor.fetchone():
                sql = """INSERT INTO {} (animatetitle, introducation, nums) VALUE (\'{}\', \'{}\', \'{}\')""".format(item["table"],item["animatetitle"],item["introducation"],item["nums"])
                self.cursor.execute(sql)                                
                self.connect.commit()
        return item

    def close_spider(self, spider):
        self.connect.close()
