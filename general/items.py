# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class level0item0(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=scrapy.Field()
    articleid=scrapy.Field()


class level0item1(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    reply=scrapy.Field()
    click=scrapy.Field()

class level1item0(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=scrapy.Field()
    content=scrapy.Field()
    author=scrapy.Field()

    

