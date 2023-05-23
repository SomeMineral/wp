# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EngRusWItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    w_Eng = scrapy.Field()
    w_Rus = scrapy.Field()
    
    

class EngRusSItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    s_Eng = scrapy.Field()
    s_Rus = scrapy.Field()
    
    s_EngRus = scrapy.Field()     