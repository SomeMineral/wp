# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VnanetURLItem(scrapy.Item):

    url = scrapy.Field()


class VnanetArticleItem(scrapy.Item):

    date = scrapy.Field()
    title = scrapy.Field()
    article = scrapy.Field()
    url = scrapy.Field()
