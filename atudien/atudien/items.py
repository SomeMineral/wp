# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AtudienWordItem(scrapy.Item):

    word = scrapy.Field()


class AtudienSentenceItem(scrapy.Item):

    sentence_kr = scrapy.Field()
    sentence_vi = scrapy.Field()

class AtudienEmptyItem(scrapy.Item):

    word = scrapy.Field()