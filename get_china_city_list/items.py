# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GetChinaCityListItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    province = scrapy.Field()
    city_url = scrapy.Field()
    city = scrapy.Field()
    district_url = scrapy.Field()
    district_code = scrapy.Field()
    district = scrapy.Field()
