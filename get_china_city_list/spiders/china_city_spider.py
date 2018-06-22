#! -*- coding:utf-8 -*-

import scrapy
from get_china_city_list.items import GetChinaCityListItem


class ChinaCity(scrapy.Spider):
    name="ChinaCity"
    allowed_domains = ['www.stats.gov.cn']

    def start_requests(self):
        urls = ["http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/index.html"]
        for item in urls:
            yield scrapy.Request(url=item, callback=self.parse_province)

    def parse_province(self, response):
        page_list = response.url.split("/")

        for item in response.css("table.provincetable tr.provincetr td"):
            prov_item = GetChinaCityListItem()
            prov_item["province"] = item.css("a::text").extract_first()
            page = item.css("a::attr(href)").extract_first()
            prov_item["city_url"] = "/".join(page_list[:-1] + [page])

            yield scrapy.Request(url=prov_item["city_url"], meta={'item': prov_item}, callback=self.parse_city)

    def parse_city(self, response):
        base_url_list = response.url.split("/")
        province = response.meta["item"]["province"]

        for item in response.css("table.citytable tr.citytr"):
            city_item = GetChinaCityListItem()
            city_item["province"] = province
            url_suffix = item.css("td a::attr(href)").extract()[1]
            city_item["city"] = item.css("td a::text").extract()[1]
            city_item["district_url"] = "/".join(base_url_list[:-1] + [url_suffix])
            city_item["city_url"] = response.url

            yield scrapy.Request(url=city_item["district_url"], meta={'item': city_item}, callback=self.parse_district)

    def parse_district(self, response):
        base_url_list = response.url.split("/")
        city_item = response.meta["item"]

        for item in response.css("table.countytable tr.countytr"):
            district_item = GetChinaCityListItem()
            district_item["province"] = city_item["province"]
            district_item["city"] = city_item["city"]

            td_text_list = item.css("td::text").extract()
            if len(td_text_list) == 2:
                district_item["district"] = td_text_list[1]
                district_item["district_code"] = item.css("td::text").extract()[0]
            else:
                district_item["district"] = item.css("td a::text").extract()[1]
                district_item["district_code"] = item.css("td a::text").extract()[0]

            yield district_item



