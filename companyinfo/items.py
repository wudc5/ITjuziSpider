# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    companylogolink = scrapy.Field()  #公司logo图片链接
    companyname = scrapy.Field()      #公司名称
    industry = scrapy.Field()         #公司行业
    establishtime = scrapy.Field()    #公司成立时间
    companylocation = scrapy.Field()  #公司位置
    finaceinfo=scrapy.Field()         #公司融资情况
    companylink=scrapy.Field()        #公司详情页链接
    companybasicinfo = scrapy.Field() #公司基本信息
    companytag = scrapy.Field()       # 公司Tag
    companysize = scrapy.Field()      #公司规模
    companystatus = scrapy.Field()    #公司现在的运行状态

    # Output=scrapy.Field()
    # Sample_Input=scrapy.Field()
    # Sample_Output=scrapy.Field()
    pass
