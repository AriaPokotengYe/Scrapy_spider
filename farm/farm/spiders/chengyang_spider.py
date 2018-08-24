# -*- coding: utf-8 -*-
import scrapy
import time
import json

from farm.items import FarmItem

class ChengyangSpiderSpider(scrapy.Spider):
    name = 'chengyang_spider'
    allowed_domains = ['www.cncyms.cn']
    current_num = 1

    def start_requests(self):
        url = 'http://www.cncyms.cn/pages.php'

        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
            url=url,
            formdata={"pageNum": "1","pname":"","reltime":"副食品" },
            callback=self.parse
        )


    def parse(self, response):
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
            yield farm_item

        self.current_num+=1
        print("=====================crawl:" + str(self.current_num))
        if self.current_num!=2942:
            yield scrapy.FormRequest(
                url='http://www.cncyms.cn/pages.php',
                formdata={"pageNum": str(self.current_num), "pname": "", "reltime": "副食品"},
                callback=self.parse
            )





