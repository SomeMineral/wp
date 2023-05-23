# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TsukubaItem(scrapy.Item):
    json_box = scrapy.Field()
    hcid = scrapy.Field()

