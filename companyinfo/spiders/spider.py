#!/usr/bin/env python
# coding=utf-8
from scrapy.spiders import Spider
from companyinfo.items import CompanyItem
from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapy.selector import Selector

class CompanySpider(Spider):
    print "***************************************************"
    name='companyinfo'
    allowed_domains=['itjuzi.com']
    print "################"
    start_urls=[]
    for i in range(1,5,1):
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
        print response.body
        with open("dfs.html", 'w') as wp:
            wp.write(response.body)
            wp.close()
        sel=Selector(response)
        sites=sel.xpath('//ul[@class="list-main-icnset list-main-com"]/li')
        print '*'*10
        print 'len(sites):',len(sites)
        for site in sites:
            item=CompanyItem()
            img_url = site.xpath('i[@class="cell pic"]/a[@target="_blank"]//img/@src').extract()[0]
            print "img_url: ", img_url
            # company_name = site.xpath('i[@class="cell maincell"]/p[@class = "title"]/a[@target="_blank"]/@href').extract()
            company_name = site.xpath('i[@class="cell maincell"]//text()').extract()
            # for company in company_name:
            print "company_name: ", company_name
            establish_time = site.xpath('i[@class="cell date"]/text()').extract()[0].replace("\n", "").replace("\t", "").replace(" ", "")
            location = site.xpath('i[@class="cell addr"]//a/text()').extract()[0]
            # finace_info = site.xpath('i[@class="cell status"]//text()').extract()
            # finace_info = finace_info[1] + finace_info[3] + finace_info[5]
            companylink = site.xpath('i[@class="cell pic"]/a[@target="_blank"]/@href').extract()[0]
            print "establish_time:", establish_time
            print "location: ", location
            # print "finacing: ", finace_info
            print "link_url: ", companylink
            # item['title']=site.xpath("text()").extract()[0]
            # item['link']=site.xpath("@href").extract()
            next_url = companylink
            # item['link']=next_url
            print next_url
            yield Request(url=next_url,meta={'item': item},callback=self.parse2)



   # def parse2(self,response):
   #     soup=BeautifulSoup(response.body)
   #     tag=soup.find("div",attrs={"class":"rich_media_content","id":"js_content"})
   #     content_list=[tag_i.text for tag_i in tag.findAll('p')]
   #     content="".join(content_list)
   #    # content='wdc'
   #     item=response.meta['item']
   #     item['content']=content
   #     return item

    def parse2(self,response):
        print response.body
        sel = Selector(response)
        Time_Limit=sel.xpath('//div[@class="plm"]/table/tr[1]/td[1]/text()').extract()[0]
        
        print "length of Time_Limit:",len(Time_Limit)
        Memory_Limit=sel.xpath('//div[@class="plm"]/table/tr[1]/td[3]/text()').extract()[0]
        print 'len(Memory_Limit)',len(Memory_Limit)
        
        DescriptionTag=sel.xpath('//div[@class="ptx"]')
        print '!'*20
        print 'length of Des:',len(DescriptionTag)
        Description=DescriptionTag[0].xpath('string(.)').extract()[0]

        InputTag=sel.xpath('//div[@class="ptx"]')
        Input=InputTag[1].xpath('string(.)').extract()[0]
        
        OutputTag=sel.xpath('//div[@class="ptx"]')
        Output=OutputTag[2].xpath('string(.)').extract()[0]
        
        Sample_InputTag=sel.xpath('//pre[@class="sio"]')
        Sample_Input=Sample_InputTag[0].xpath('string(.)').extract()[0]
        
        Sample_OutputTag=sel.xpath('//pre[@class="sio"]')
        Sample_Output=Sample_OutputTag[1].xpath('string(.)').extract()[0]

        print 'length of Sample_InputTag:',len(Sample_InputTag)
        item=response.meta['item']
        item['Time_Limit']=Time_Limit
        item['Memory_Limit']=Memory_Limit
        item['Description']=Description
        item['Input']=Input
        item['Output']=Output

        item['Sample_Input']=Sample_Input

        item['Sample_Output']=Sample_Output
        return item
