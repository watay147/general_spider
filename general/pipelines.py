# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import time
import re
class DBPipeline(object):

    def open_spider(self, spider):
        self.storeFunc={'XMulItem':self.storeXMulItem,
			'XSinItem':self.storeXSinItem,
			'YMulItem':self.storeYMulItem,
			'YSinItem':self.storeYSinItem,
			'ZMulItem':self.storeZMulItem,
			'ZSinItem':self.storeZSinItem,
			}
        self.conn = MySQLdb.Connect( user='root',  db='guba',charset='utf8')
        self.cursor=self.conn.cursor() 
        self.crawldate=time.strftime("%Y-%m-%d",time.localtime())
        self.stockno=re.search(r',\d+',spider.start_urls[0]).group(0)[1:]

    def process_item(self, item, spider):
        
        if len(item)!=0:
            self.storeFunc[item.__class__.__name__](item)
        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()
        spider.browser.close()
        spider.f.close()
        print "finish!"

    def storeXMulItem(self,item):
        itemlist=zip(item['Xtitle'],item['Xarticleid'],item['Xstockno'],item['Xreply'],item['Xclick'])
        for instance in itemlist:
            instance=instance+(self.crawldate,)
            self.cursor.execute("insert ignore into `gubarticleupdate%s` (title,articleid,stockno,reply,click,crawldate) value ('%s',%s,'%s',%s,%s,'%s')"% ((self.stockno,)+instance))
            
        self.conn.commit()
        




    def storeXSinItem(self,item):
        pass
        

    def storeYMulItem(self,item):
        itemlist=zip(item['YcommentAuthor'],item['YcommentDate'],item['YcommentContent'],item['YcommentAuthorid'],item['Yarticleid'])
        for instance in itemlist:
            self.cursor.execute("insert ignore into `reply%s` (commentAuthor,commentDate,commentContent,commentAuthorid,articleid) value ('%s','%s','%s',%s,%s)"% ((self.stockno,)+instance))
        self.conn.commit()
      

    def storeYSinItem(self,item):
        instance=(item['Ytitle'],item['Yauthor'],item['Ystockno'],item['Ydate'],item['Ycontent'],item['Yarticleid'])
        self.cursor.execute("insert ignore into `article%s` (title,author,stockno,time,content,articleid) value ('%s','%s','%s','%s','%s',%s)"% ((self.stockno,)+instance))#insert ignore会自动避免重复插入
        self.conn.commit()
        

    def storeZMulItem(self,item):
        itemlist=zip(item['ZcommentAuthor'],item['ZcommentDate'],item['ZcommentContent'],item['ZcommentAuthorid'],item['Zarticleid'])
        for instance in itemlist:
            self.cursor.execute("insert ignore into `reply%s` (commentAuthor,commentDate,commentContent,commentAuthorid,articleid) value ('%s','%s','%s',%s,%s)"% (self.stockno,)+instance)
        
        self.conn.commit()
    

    def storeZSinItem(self,item):
        pass



