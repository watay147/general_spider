# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

class DBPipeline(object):
    def open_spider(self, spider):
        self.testf=open('testf.txt','w')
        self.storeFunc={'XMulItem':self.storeXMulItem,
			'XSinItem':self.storeXSinItem,
			'YMulItem':self.storeYMulItem,
			'YSinItem':self.storeYSinItem,
			'ZMulItem':self.storeZMulItem,
			'ZSinItem':self.storeZSinItem,
			}
        self.conn = MySQLdb.Connect( user='root',  db='testdb',charset='utf8')
        self.cursor=self.conn.cursor() 

    def process_item(self, item, spider):
        if len(item)!=0:
            self.storeFunc[item.__class__.__name__](item)
        return item

    def close_spider(self,spider):
        self.testf.close()
        self.cursor.close()
        self.conn.close()
        spider.browser.close()
        print "finish!"

    def storeXMulItem(self,item):
        itemlist=zip(item['Xtitle'],item['Xauthor'],item['Xreply'],item['Xclick'])
        for instance in itemlist:
            self.cursor.execute("insert into lab (title,author,reply,click) value ('%s','%s',%s,%s)"% instance)
            self.conn.commit()




    def storeXSinItem(self,item):
        pass

    def storeYMulItem(self,item):
        pass

    def storeYSinItem(self,item):
        pass

    def storeZMulItem(self,item):
        pass

    def storeZSinItem(self,item):
        pass



