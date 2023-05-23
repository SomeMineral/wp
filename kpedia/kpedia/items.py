# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KpediaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    kr_sen = scrapy.Field()
    jp_sen = scrapy.Field()

class KpediaWordItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    word = scrapy.Field()
