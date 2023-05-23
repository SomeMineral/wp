# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TechdicoItem(scrapy.Item):
    kor = scrapy.Field()
    eng = scrapy.Field()