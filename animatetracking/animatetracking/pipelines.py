# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from scrapy.exceptions import NotConfigured
from animatetracking.items import AnimatelistItem
from animatetracking import settings

DEBUG = 0
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
        #create new table 
        sql = """SELECT COUNT(*) FROM information_schema.tables WHERE table_name = \'"""+item["table"]+ """\'"""         
        self.cursor.execute(sql)
        if self.cursor.fetchone()[0] == 0:
            sql = "CREATE TABLE " +item["table"]+" (id INT AUTO_INCREMENT PRIMARY KEY, animatetitle VARCHAR(255), othertitle text, cross_s VARCHAR(255), nums INT, last_title VARCHAR(255))"
            self.cursor.execute(sql)
            sql = "ALTER TABLE " + item["table"]+ " CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci"
            self.cursor.execute(sql)

        sql = """select * from {} where animatetitle = \'{}\'""".format(item["table"],item["animatetitle"])
        self.cursor.execute(sql)
        if not self.cursor.fetchone():
            sql = """INSERT INTO {} (animatetitle, othertitle, cross_s, nums, last_title) VALUE (\'{}\',\'{}\',\'{}\', \'{}\',\'{}\')""".format(item["table"],item["animatetitle"],item["othertitle"],item["cross"],item["nums"],item["last_title"])
            self.cursor.execute(sql)                                
            self.connect.commit()
        return item

    def close_spider(self, spider):
        self.connect.close()
