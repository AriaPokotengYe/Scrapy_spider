# -*- coding: utf-8 -*-
import scrapy
import time
import datetime
from farm.items import FarmItem
#运行命令: scrapy crawl auto_vipveg_spider -o ./data/vipveg.csv
#本爬虫自动爬取所有省份所有市场所有品种的第一页价格页面



class AutoVipvegSpiderSpider(scrapy.Spider):
    now = time.strftime('%Y-%m-%d', time.localtime())
    #爬虫开始时间的时间戳
    today = time.time()
    #爬取从当前时间开始往前20天内的数据
    crawl_day = 20*24*60*60
    name = 'auto_vipveg_spider'
    allowed_domains = ['www.vipveg.com']
    start_urls = ['http://www.vipveg.com/market/cta-1.html']

    def getArea(self, province):
        if (province== "山东" or province== "江苏" or province== "安徽" or province== "浙江" or province== "福建" or province== "上海"):
            return "华东"
        if (province== "广东" or province== "广西" or province== "海南"):
            return "华南"
        if (province== "湖北" or province== "湖南" or province== "河南" or province== "江西"):
            return "华中"
        if (province== "北京" or province== "天津" or province== "河北" or province== "山西" or province== "内蒙古"):
            return "华北"
        if (province== "宁夏" or province== "新疆" or province== "青海" or province== "陕西" or province== "甘肃"):
            return "西北"
        if (province== "四川" or province== "云南" or province== "贵州" or province== "西藏" or province== "重庆"):
            return "西南"
        if (province== "辽宁" or province== "吉林" or province== "黑龙江"):
            return "东北"
        if (province== "台湾" or province== "香港" or province== "澳门"):
            return "港澳台"
        return "异常"

    def parse(self, response):
        print("----------正在解析首页-----------")
        item_list = response.xpath("//td[@class='borderTop p_5']/table/tr/td/a")
        # print(item_list)
        for i_item in item_list:
            city = i_item.xpath("./text()").extract_first()
            area = self.getArea(city)
            farm_item = FarmItem()
            farm_item['province'] = city
            farm_item['area'] = area
            farm_item['typy'] = "蔬菜"
            farm_item['standard'] = "none"
            farm_item['color'] = "none"
            farm_item['unit'] = "元/斤"
            farm_item['entertime'] = self.now
            if area != "异常":
                yield scrapy.Request("http://www.vipveg.com" + i_item.xpath("./@href").extract_first(),
                                     meta={'item': farm_item},
                                     callback=self.provinceIndexParse)



    def provinceIndexParse(self, response):
        print("----------正在解析省份目录页-----------")
        farm_item = response.meta['item']
        # print(farm_item)
        item_list = response.xpath("//table[@class='m_t_5']")
        for item in item_list:
            farm_item['market'] = item.xpath("./tr/td[2]/p[1]/a/text()").extract_first()
            yield scrapy.Request("http://www.vipveg.com" + item.xpath("./tr/td[2]/p[1]/a/@href").extract_first(),
                                 meta={'item': farm_item},
                                 callback=self.marketIndexParse)


    def marketIndexParse(self, response):
        print("----------正在解析市场首页-----------")
        farm_item = response.meta['item']
        item_list = response.xpath("//td[@class='borderTop p_3_4 l_h_21']/table/tr")
        # print(item_list)
        for i_item in item_list:
            if i_item.xpath("./td[1]/a/@href").extract_first():
                yield scrapy.Request("http://www.vipveg.com" + i_item.xpath("./td[1]/a/@href").extract_first(),
                                     meta={'item': farm_item},
                                     callback=self.pricePage_parse)

            if i_item.xpath("./td[2]/a/@href").extract_first():
                yield scrapy.Request("http://www.vipveg.com" + i_item.xpath("./td[2]/a/@href").extract_first(),
                                     meta={'item': farm_item},
                                     callback=self.pricePage_parse)

            if i_item.xpath("./td[3]/a/@href").extract_first():
                yield scrapy.Request("http://www.vipveg.com" + i_item.xpath("./td[3]/a/@href").extract_first(),
                                     meta={'item': farm_item},
                                     callback=self.pricePage_parse)


    def pricePage_parse(self, response):
        #解析价格页面
        farm_item = response.meta['item']
        item_list = response.xpath("//table[@class='f_s_14']/tr")
        for i_item in item_list:
            farm_item['name'] = i_item.xpath("./td[5]/a/text()").extract_first()[11:-4]
            farm_item['minPrice'] = i_item.xpath("./td[2]/text()").extract_first()[1:]
            farm_item['avgPrice'] = i_item.xpath("./td[4]/text()").extract_first()[1:]
            farm_item['maxPrice'] = i_item.xpath("./td[3]/text()").extract_first()[1:]
            farm_item['time'] = i_item.xpath("./td[1]/text()").extract_first()
            #如果在爬取相应的时间范围内，则加入item
            if time.mktime(time.strptime(farm_item['time'], "%Y-%m-%d")) > self.today-self.crawl_day:
                yield farm_item
