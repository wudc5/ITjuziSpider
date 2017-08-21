#!/usr/bin/env python
# coding=utf-8
from scrapy.spiders import Spider
from companyinfo.items import CompanyItem
from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapy.selector import Selector

class CompanySpider(Spider):
    print "***************************************************"
    name = 'companyinfo'
    allowed_domains = ['itjuzi.com']
    start_urls = []
    for i in range(1, 20, 1):
        start_urls.append('https://www.itjuzi.com/company?page=%d'% i)
        # start_urls.append('https://www.itjuzi.com/investevents?page=%d'% i)
        # 'https://www.itjuzi.com/investevents?page=2'
    print "start_urls", start_urls
    #start_urls=['http://poj.org/problemlist?volume=2']
    # def start_requests(self):
    #    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'}
    #    print 'here'*10
    #    yield Request('https://www.itjuzi.com/company?page=1',headers=headers,callback=self.parse)


#    def parse(self,response):
#    #    item=PojItem()
#    #    item['title']='hello word'
#    #    item['link']='www.'
#    #    item['content']='wdcwdc'
#    #    return item
#        soup=BeautifulSoup(response.body)
#        tags=soup.findAll("td",attrs={"align":"left"})
#        print 'tags:',tags
#        print '!'*10
#        for tag in tags:
#            item=PojItem()
#            item['title']=tag.text
#            item['link']=tag.find('a').get('href')
#            next_url='http://poj.org/'+item['link']
#            print next_url
#            yield Request(url=next_url,meta={'item':item},callback=self.parse2)

    def parse(self,response):
        sel=Selector(response)
        sites=sel.xpath('//ul[@class="list-main-icnset list-main-com"]/li')
        print '*'*10
        print 'len(sites):',len(sites)
        for site in sites:
            item = CompanyItem()
            try:
                finaceinfo = site.xpath('i[@class="cell status"]//text()').extract()
                finaceinfo = "".join(finaceinfo).replace("\n", "").replace("\t", "").replace(" ", "")
            except:
                finaceinfo = "暂未收录融资信息"
            item['finaceinfo'] = finaceinfo
            try:
                item['companylink'] = site.xpath('i[@class="cell pic"]/a[@target="_blank"]/@href').extract()[0]
            except:
                item['companylink'] = "无公司链接"
            next_url = item['companylink']
            print next_url
            yield Request(url=next_url, meta={'item': item},callback=self.parse2)



   # def parse2(self,response):
   #     soup=BeautifulSoup(response.body)
   #     tag=soup.find("div",attrs={"class":"rich_media_content","id":"js_content"})
   #     content_list=[tag_i.text for tag_i in tag.findAll('p')]
   #     content="".join(content_list)
   #    # content='wdc'
   #     item=response.meta['item']
   #     item['content']=content
   #     return item

    def parse2(self, response):
        sel = Selector(response)
        try:
            companylogolink = sel.xpath('//div[@class="on-edit-hide"]/div[@class="rowhead"]/div[@class="pic"]/img/@src').extract()[0]
        except:
            companylogolink = "无公司logo图片"

        try:
            industry = sel.xpath('//div[@class="rowhead"]//span[@class="scope c-gray-aset"]/a/text()').extract()[0]
        except:
            industry = "无行业介绍"

        try:
            companylocation = sel.xpath('//div[@class="rowhead"]//span[@class="loca c-gray-aset"]//text()').extract()
            companylocation = "".join(companylocation).replace("\n", "").replace("\t", "").replace(" ", "")
        except:
            companylocation = "无公司地址"
        try:
            companytag = sel.xpath('//div[@class="rowfoot"]/div[@class="tagset dbi c-gray-aset"]//span/text()').extract()
            companytag = "、".join(companytag)
        except:
            companytag = "无Tag"
        try:
            basicinfo = sel.xpath('//div[@class="block-inc-info on-edit-hide"]/div[2]//text()').extract()
            companybasicinfo = ""
            max = 0
            for info in basicinfo:
                info = info.replace("\n", "").replace("\t", "").replace(" ", "")
                if "购买数据请联系hello@itjuzi.com" not in info and len(info) > max:
                    companybasicinfo = info
                    max = len(info)
            # if len(basicinfo) > 1:
            #     companybasicinfo = (";".join(basicinfo)+"&&&"+basicinfo[1]).replace("\n", "").replace("\t", "").replace(" ", "")
            # else:
            #     companybasicinfo = (";".join(basicinfo)+"&&&"+basicinfo[0]).replace("\n", "").replace("\t", "").replace(" ", "")
        except:
            companybasicinfo = "无基本信息"
        try:
            companyname = sel.xpath('//div[@class="block-inc-info on-edit-hide"]//div[@class="des-more"]//h2[@class="seo-second-title"]/text()').extract()[0]
            namesplit = companyname.split("：")
            if '暂未收录'in namesplit[1]:
                companyname = sel.xpath('//div[@class="rowhead"]//div[@class="picinfo"]//span[@class="title"]/h1/text()').extract()[0].replace("\n", "").replace("\t", "").replace(" ", "")
            else:
                companyname = namesplit[1]
        except:
            companyname = "无公司名字"
        try:
            establishtime = sel.xpath('//div[@class="block-inc-info on-edit-hide"]//div[@class="des-more"]//h2[@class="seo-second-title"]/text()').extract()[1]
            establishtime = establishtime.split("：")[1]
        except:
            establishtime = "无成立时间"
        try:
            companysize = sel.xpath('//div[@class="block-inc-info on-edit-hide"]//div[@class="des-more"]//h2[@class="seo-second-title"]/text()').extract()[2]
            companysize = companysize.replace("\n", "").replace("\t", "").replace(" ", "").split("：")[1]
        except:
            companysize = "无公司规模"
        try:
            companystatus = sel.xpath('//div[@class="block-inc-info on-edit-hide"]/div[3]/div[1]/div[3]/span/text()').extract()[0]
        except:
            companystatus = "无公司状态"

        #
        # print "companylogolink: ", companylogolink
        # print "industry: ", industry
        # print "companylocation: ", companylocation
        # print "companytag: ", companytag
        # print "companybasicinfo: ", companybasicinfo
        # print "companyname: ", companyname
        # print "establishtime: ", establishtime
        # print "companysize: ", companysize
        # print "companystatus: ", companystatus

        item = response.meta['item']
        item['companylogolink'] = companylogolink
        item['industry'] = industry
        item['companylocation'] = companylocation
        item['companytag'] = companytag
        item['companybasicinfo'] = companybasicinfo
        item['companyname'] = companyname
        item['establishtime'] = establishtime
        item['companysize'] = companysize
        item['companystatus'] = companystatus

        # Time_Limit=sel.xpath('//div[@class="plm"]/table/tr[1]/td[1]/text()').extract()[0]
        #
        # print "length of Time_Limit:",len(Time_Limit)
        # Memory_Limit=sel.xpath('//div[@class="plm"]/table/tr[1]/td[3]/text()').extract()[0]
        # print 'len(Memory_Limit)',len(Memory_Limit)
        #
        # DescriptionTag=sel.xpath('//div[@class="ptx"]')
        # print '!'*20
        # print 'length of Des:',len(DescriptionTag)
        # Description=DescriptionTag[0].xpath('string(.)').extract()[0]
        #
        # InputTag=sel.xpath('//div[@class="ptx"]')
        # Input=InputTag[1].xpath('string(.)').extract()[0]
        #
        # OutputTag=sel.xpath('//div[@class="ptx"]')
        # Output=OutputTag[2].xpath('string(.)').extract()[0]
        #
        # Sample_InputTag=sel.xpath('//pre[@class="sio"]')
        # Sample_Input=Sample_InputTag[0].xpath('string(.)').extract()[0]
        #
        # Sample_OutputTag=sel.xpath('//pre[@class="sio"]')
        # Sample_Output=Sample_OutputTag[1].xpath('string(.)').extract()[0]
        #
        # print 'length of Sample_InputTag:',len(Sample_InputTag)
        # item['Time_Limit']=Time_Limit
        # item['Memory_Limit']=Memory_Limit
        # item['Description']=Description
        # item['Input']=Input
        # item['Output']=Output
        #
        # item['Sample_Input']=Sample_Input
        #
        # item['Sample_Output']=Sample_Output
        return item
