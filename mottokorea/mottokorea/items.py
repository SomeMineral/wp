# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MottokoreaErrorItem(scrapy.Item):
    error_url = scrapy.Field()


class MottokoreaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    kr_expr = scrapy.Field()
    jp_mean = scrapy.Field()
