# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    img_url = scrapy.Field()
    company_name = scrapy.Field()
    establish_time = scrapy.Field()
    location = scrapy.Field()
    finace_info=scrapy.Field()
    companylink=scrapy.Field()
    # Output=scrapy.Field()
    # Sample_Input=scrapy.Field()
    # Sample_Output=scrapy.Field()
    pass
