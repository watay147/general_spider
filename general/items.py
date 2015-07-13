# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XMulItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Xtitle=scrapy.Field()
    Xauthor=scrapy.Field()
    Xreply=scrapy.Field()
    Xclick=scrapy.Field()

class XSinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Xtitle=scrapy.Field()
    Xauthor=scrapy.Field()
    Xreply=scrapy.Field()
    Xclick=scrapy.Field()

class YMulItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    YcommentAuthor=scrapy.Field()
    YcommentDate=scrapy.Field()
    YcommentContent=scrapy.Field()

class YSinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Ycontent=scrapy.Field()
    Ydate=scrapy.Field()
    

class ZMulItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ZcommentAuthor=scrapy.Field()
    ZcommentDate=scrapy.Field()
    ZcommentContent=scrapy.Field()

class ZSinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ZcommentAuthor=scrapy.Field()
    ZcommentDate=scrapy.Field()
    ZcommentContent=scrapy.Field()
    

