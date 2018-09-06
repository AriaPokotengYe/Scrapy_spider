# -*- coding: utf-8 -*-
import scrapy
import time
import json
from farm.items import FarmItem

#运行命令: scrapy crawl auto_chengyang_spider -o ./data/chengyang.csv

class AutoChengyangSpiderSpider(scrapy.Spider):
    name = 'auto_chengyang_spider'
    allowed_domains = ['www.cncyms.cn']
    #最大爬取页数，必须大于等于2
    max_crawl_num = 20
    # 爬虫开始时间的时间戳
    today = time.time()
    # 爬取从当前时间开始往前2天内的数据
    crawl_day = 2 * 24 * 60 * 60

    shucai_current_num = 1
    shuichanpin_current_num = 1
    guopin_current_num = 1
    fushipin_current_num = 1

    def start_requests(self):
        url = 'http://www.cncyms.cn/pages.php'

        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
            url=url,
            formdata={"pageNum": "1","pname":"","reltime":"蔬菜" },
            callback=self.shucai_parse
        )
        yield scrapy.FormRequest(
            url=url,
            formdata={"pageNum": "1", "pname": "", "reltime": "水产品"},
            callback=self.shuichanpin_parse
        )
        yield scrapy.FormRequest(
            url=url,
            formdata={"pageNum": "1", "pname": "", "reltime": "果品"},
            callback=self.guopin_parse
        )
        yield scrapy.FormRequest(
            url=url,
            formdata={"pageNum": "1", "pname": "", "reltime": "副食品"},
            callback=self.fushipin_parse
        )

    def shucai_parse(self, response):
        now = time.strftime('%Y-%m-%d', time.localtime())
        json_response = json.loads(response.body)
        for num in range(0, 18):
            farm_item = FarmItem()
            farm_item['province'] = "山东"
            farm_item['market'] = "青岛市城阳蔬菜水产品批发市场"
            farm_item['typy'] = json_response["list"][num]["PSort"]
            farm_item['name'] = json_response["list"][num]["PName"]
            farm_item['standard'] = "none"
            farm_item['area'] = "华东"
            farm_item['color'] = "none"
            farm_item['unit'] = "元/公斤"
            farm_item['minPrice'] = json_response["list"][num]["LPrice"]
            farm_item['avgPrice'] = json_response["list"][num]["PPrice"]
            farm_item['maxPrice'] = json_response["list"][num]["MPrice"]
            farm_item['entertime'] = now
            farm_item['time'] = json_response["list"][num]["ReleaseTime"]
            if time.mktime(time.strptime(farm_item['time'], "%Y-%m-%d")) > self.today - self.crawl_day:
                yield farm_item
            # yield farm_item
        self.shucai_current_num += 1
        if self.shucai_current_num != self.max_crawl_num:
            yield scrapy.FormRequest(
                url='http://www.cncyms.cn/pages.php',
                formdata={"pageNum": str(self.shucai_current_num), "pname": "", "reltime": "蔬菜"},
                callback=self.shucai_parse
            )

    def shuichanpin_parse(self, response):
        now = time.strftime('%Y-%m-%d', time.localtime())
        json_response = json.loads(response.body)
        for num in range(0, 18):
            farm_item = FarmItem()
            farm_item['province'] = "山东"
            farm_item['market'] = "青岛市城阳蔬菜水产品批发市场"
            farm_item['typy'] = json_response["list"][num]["PSort"]
            farm_item['name'] = json_response["list"][num]["PName"]
            farm_item['standard'] = "none"
            farm_item['area'] = "华东"
            farm_item['color'] = "none"
            farm_item['unit'] = "元/公斤"
            farm_item['minPrice'] = json_response["list"][num]["LPrice"]
            farm_item['avgPrice'] = json_response["list"][num]["PPrice"]
            farm_item['maxPrice'] = json_response["list"][num]["MPrice"]
            farm_item['entertime'] = now
            farm_item['time'] = json_response["list"][num]["ReleaseTime"]
            if time.mktime(time.strptime(farm_item['time'], "%Y-%m-%d")) > self.today - self.crawl_day:
                yield farm_item
            # yield farm_item
        self.shuichanpin_current_num += 1
        if self.shuichanpin_current_num != self.max_crawl_num:
            yield scrapy.FormRequest(
                url='http://www.cncyms.cn/pages.php',
                formdata={"pageNum": str(self.shuichanpin_current_num), "pname": "", "reltime": "水产品"},
                callback=self.shuichanpin_parse
            )

    def guopin_parse(self, response):
        now = time.strftime('%Y-%m-%d', time.localtime())
        json_response = json.loads(response.body)
        for num in range(0, 18):
            farm_item = FarmItem()
            farm_item['province'] = "山东"
            farm_item['market'] = "青岛市城阳蔬菜水产品批发市场"
            farm_item['typy'] = json_response["list"][num]["PSort"]
            farm_item['name'] = json_response["list"][num]["PName"]
            farm_item['standard'] = "none"
            farm_item['area'] = "华东"
            farm_item['color'] = "none"
            farm_item['unit'] = "元/公斤"
            farm_item['minPrice'] = json_response["list"][num]["LPrice"]
            farm_item['avgPrice'] = json_response["list"][num]["PPrice"]
            farm_item['maxPrice'] = json_response["list"][num]["MPrice"]
            farm_item['entertime'] = now
            farm_item['time'] = json_response["list"][num]["ReleaseTime"]
            if time.mktime(time.strptime(farm_item['time'], "%Y-%m-%d")) > self.today - self.crawl_day:
                yield farm_item
            # yield farm_item
        self.guopin_current_num += 1
        if self.guopin_current_num != self.max_crawl_num:
            yield scrapy.FormRequest(
                url='http://www.cncyms.cn/pages.php',
                formdata={"pageNum": str(self.guopin_current_num), "pname": "", "reltime": "果品"},
                callback=self.guopin_parse
            )

    def fushipin_parse(self, response):
        now = time.strftime('%Y-%m-%d', time.localtime())
        json_response = json.loads(response.body)
        for num in range(0, 18):
            farm_item = FarmItem()
            farm_item['province'] = "山东"
            farm_item['market'] = "青岛市城阳蔬菜水产品批发市场"
            farm_item['typy'] = json_response["list"][num]["PSort"]
            farm_item['name'] = json_response["list"][num]["PName"]
            farm_item['standard'] = "none"
            farm_item['area'] = "华东"
            farm_item['color'] = "none"
            farm_item['unit'] = "元/公斤"
            farm_item['minPrice'] = json_response["list"][num]["LPrice"]
            farm_item['avgPrice'] = json_response["list"][num]["PPrice"]
            farm_item['maxPrice'] = json_response["list"][num]["MPrice"]
            farm_item['entertime'] = now
            farm_item['time'] = json_response["list"][num]["ReleaseTime"]
            # 如果在爬取相应的时间范围内，则加入item
            if time.mktime(time.strptime(farm_item['time'], "%Y-%m-%d")) > self.today - self.crawl_day:
                yield farm_item
            # yield farm_item
        self.fushipin_current_num += 1
        if self.fushipin_current_num != self.max_crawl_num:
            yield scrapy.FormRequest(
                url='http://www.cncyms.cn/pages.php',
                formdata={"pageNum": str(self.fushipin_current_num), "pname": "", "reltime": "副食品"},
                callback=self.fushipin_parse
            )
