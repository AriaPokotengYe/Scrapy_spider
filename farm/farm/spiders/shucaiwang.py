 # -*- coding: utf-8 -*-
import scrapy
import time
from farm.items import FarmItem

class shucaiwang(scrapy.Spider):
    now=time.strftime('%Y-%m-%d',time.localtime())
    name='shucaiwang_spider'
    allowed_domains=['www.vegnet.com.cn']
    start_urls=['http://www.vegnet.com.cn/']

    def parse(self, response):
        item_list = response.xpath("//a[@class='channelid']")
        for i_item in item_list :
            print(item_list.xpath("./text())").extract_first()+"进入抓取序列")
            yield scrapy.Request("http://www.vegnet.com.cn/"+i_item.xpath("./@href").extrac_first(),
                                 callback=self.priceRequest_parse)

    def priceRequest_parse(self,reponse):
        print("获取价格页面")
        item_page=reponse.xpath("//a[@href='/Channel/Price?flag=12&ename=fanqie']")
        yield scrapy.Request("http://www.vegnet.com.cn/"+item_page.xpath("./@href").extrac_first(),
                             callback=self.priceCrawl_parse)

    def priceCrawl_prase(self,reponse):
        print("~~~~~准备抓取数据~~~~~")
        item_list