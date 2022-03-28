# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

#import pymysql
from scrapy.exceptions import NotConfigured
from animatetracking.items import AnimatelistItem
from animatetracking import settings
import csv
import pandas as pd
import os.path 


DEBUG = 0
basePath='/home/liang/hdd/d5/animate'
class AnimatetrackingPipeline(object):
    def __init__(self):
        # remove SQL support
        #self.connect = pymysql.connect(
        #    host=settings.MYSQL_HOST,
        #    db=settings.MYSQL_DBNAME,
        #    user=settings.MYSQL_USER,
        #    passwd=settings.MYSQL_PASSWD,
        #    charset='utf8',
        #    use_unicode=True)
        #self.cursor = self.connect.cursor()
        # use csv to store data
        self.pd_dict={}

    def process_item(self, item, spider):
        # remove SQL support
        '''
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
        '''
        # use csv to store data
        #check whether table already exsit in pd_dict
        if item["table"] not in self.pd_dict:
            #check whether csv with table name exit
            file = basePath +'/'+ item["table"]+'.csv'
            if os.path.exists(file):
                df = pd.read_csv(file)
                self.pd_dict.update({item["table"]: df})
            else:
                df = pd.DataFrame(columns = ['animatetitle', 'othertitle', 'cross_s','nums', 'last_title'])
                self.pd_dict.update({item["table"]: df})

        if item['animatetitle'] not in self.pd_dict[item["table"]]['animatetitle'].values:
            self.pd_dict[item["table"]] = self.pd_dict[item["table"]].append(
                {'animatetitle' : item['animatetitle'], 'othertitle' : item['othertitle'], 'cross_s' : item['cross'],'nums':item['nums'], 'last_title':item['last_title']}, 
                ignore_index = True)

        return item

    def close_spider(self, spider):
        for table in self.pd_dict:
            file = basePath +'/'+table+'.csv'
            self.pd_dict[table].to_csv(file, index=False)#encoding='utf-8'
        #self.connect.close()
