# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import pandas as pd
import csv
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class CompanyinfoPipeline(object):
    def __init__(self):
        self.file = open('companyinfo.csv','a')
    def process_item(self, item, spider):
        open_file_object = csv.writer(self.file)
        open_file_object.writerow([item["companyname"], item["companylogolink"],
                                   item["companylink"], item["industry"],
                                   item["establishtime"], item["companylocation"],
                                   item["finaceinfo"], item["companybasicinfo"],
                                   item["companytag"], item["companysize"],
                                   item["companystatus"]])
        #line=json.dumps(dict(item))+"\n"
        #self.file.write(line.decode('unicode_escape'))
        return item


#存储到mysql
#import MySQLdb
#import MySQLdb.cursors
#import logging
#from twisted.enterprise import adbapi
#
#class PojPipeline(object):
#    def __init__(self):
#        self.dbpool = adbapi.ConnectionPool(
#                dbapiName ='MySQLdb',
#                host ='127.0.0.1',
#                db = 'PojProblems',
#                user = 'root',
#                passwd = '123456',
#                cursorclass = MySQLdb.cursors.DictCursor,
#                charset = 'utf8',
#                use_unicode = False
#        )
#
#    # pipeline dafault function
#    def process_item(self, item, spider):
#        query = self.dbpool.runInteraction(self._conditional_insert, item)
#        logging.debug(query)
#        return item
#
#
#    # insert the data to databases
#    def _conditional_insert(self, tx, item):
#        parms = (item["title"],item["link"],item["Time_Limit"],item["Memory_Limit"],item["Description"],item["Input"],item["Output"],item["Sample_Input"],item["Sample_Output"])
#       # sql='insert into problems values("item["title"]","item["link"]","item["Time_Limit"]","item["Memory_Limit"]","item["Description"]","item["Input"]","item["Output"]","item["Sample_Input"]","item["Sample_Output"]")'
#        sql = 'insert into problems values("%s","%s","%s","%s","%s","%s","%s","%s","%s")' % parms
#        #logging.debug(sql)
#        tx.execute(sql)
