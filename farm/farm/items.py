# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FarmItem(scrapy.Item):
    # define the fields for your item here like:
    #定义结构化数据信息
    # name = scrapy.Field()
    #省份
    province = scrapy.Field()
    #市场名
    market = scrapy.Field()
    #品类
    typy = scrapy.Field()
    #品名
    name = scrapy.Field()
    #标准品名
    standard = scrapy.Field()
    #地区名
    area = scrapy.Field()
    #颜色
    color = scrapy.Field()
    #单位
    unit = scrapy.Field()
    #最低价
    minPrice = scrapy.Field()
    #均价
    avgPrice = scrapy.Field()
    #最高价
    maxPrice = scrapy.Field()
    #收录时间
    entertime = scrapy.Field()
    #计价时间
    time = scrapy.Field()