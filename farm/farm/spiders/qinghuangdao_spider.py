# -*- coding: utf-8 -*-
import scrapy
import time
from farm.items import FarmItem

class QinghuangdaoSpiderSpider(scrapy.Spider):
    now = time.strftime('%Y-%m-%d', time.localtime())
    name = 'qinghuangdao_spider'
    allowed_domains = ['www.vipveg.com']
    start_urls = ['http://www.vipveg.com/market/237.html']

    def parse(self, response):
        item_list = response.xpath("//td[@class='borderTop p_3_4 l_h_21']/table/tr")
        print(item_list)
        for i_item in item_list:
            print(i_item.xpath("./td[1]/a/text()").extract_first()+"进入抓取序列-------------")
            yield scrapy.Request("http://www.vipveg.com" + i_item.xpath("./td[1]/a/@href").extract_first(),
                                 callback=self.pricePage_parse)


            if i_item.xpath("./td[2]/a/@href").extract_first():
                print(i_item.xpath("./td[2]/a/text()").extract_first() + "进入抓取序列-------------")
                yield scrapy.Request("http://www.vipveg.com" + i_item.xpath("./td[2]/a/@href").extract_first(),
                                     callback=self.pricePage_parse)

            if i_item.xpath("./td[3]/a/@href").extract_first():
                print(i_item.xpath("./td[3]/a/text()").extract_first() + "进入抓取序列-------------")
                yield scrapy.Request("http://www.vipveg.com" + i_item.xpath("./td[3]/a/@href").extract_first(),
                                     callback=self.pricePage_parse)






    def pricePage_parse(self, response):
        print("------价格页面解析函数------")
        item_list = response.xpath("//table[@class='f_s_14']/tr")
        for i_item in item_list:
            farm_item = FarmItem()
            farm_item['province'] = "甘肃"
            farm_item['market'] = "甘肃酒泉春光农产品市场有限责任公司"
            farm_item['typy'] = "蔬菜"
            farm_item['name'] = i_item.xpath("./td[5]/a/text()").extract_first()[11:-4]
            farm_item['standard'] = "none"
            farm_item['area'] = "西北"
            farm_item['color'] = "none"
            farm_item['unit'] = "元/斤"
            farm_item['minPrice'] = i_item.xpath("./td[2]/text()").extract_first()[1:]
            farm_item['avgPrice'] = i_item.xpath("./td[4]/text()").extract_first()[1:]
            farm_item['maxPrice'] = i_item.xpath("./td[3]/text()").extract_first()[1:]
            farm_item['entertime'] = self.now
            farm_item['time'] = i_item.xpath("./td[1]/text()").extract_first()
            #print(farm_item)
            yield farm_item

        current_page = response.xpath("//div[@id='pager']/strong/text()").extract_first()
        print("正在补充当前品种的所有url")
        page_list = response.xpath("//div[@id='pager']/a")
        for page in page_list:
            yield scrapy.Request("http://www.vipveg.com" + page.xpath("./@href").extract_first(),
                                 callback=self.pricePage_parse)
        # if current_page=="1":
        #     print("第一页，正在补充当前品种的所有url")
        #     page_list = response.xpath("//div[@id='pager']/a")
        #     for page in page_list:
        #         yield scrapy.Request("http://www.vipveg.com" + page.xpath("./@href").extract_first(),
        #                              callback=self.pricePage_parse)









