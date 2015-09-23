# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import ConfigParser
import time
import re
class DBPipeline(object):

    def open_spider(self, spider):
        #Fetch the existing conf for convience from the spider object which had been initinalized.
        conf=spider.conf
        self.levels=spider.levels
        self.prefix=[]
        self.suffix=[]
        for index in range(int(self.levels)):
            self.prefix.append({ itemdef:prefix.strip("\"").strip("\'") for itemdef,prefix in conf.items("level"+str(index)+"dbprefix")})
            #dbsuffix is not necessary to be set explicitly. If it is not set, an empty dict is appended as a placeholder.
            if conf.has_section("level"+str(index)+"dbsuffix"):
                if conf.items("level"+str(index)+"dbsuffix"):
                    self.suffix.append({ itemdef:suffix.strip("\"").strip("\'") for itemdef,suffix in conf.items("level"+str(index)+"dbsuffix")})
                else:
                    self.suffix.append({})
            else:
                 self.suffix.append({})


        #Configure and initinalize the database connection based on the config file.
        confuser=conf.get('basic','dbuser').strip("\"").strip("\'")
        confdb=conf.get('basic','dbname').strip("\"").strip("\'")
        confpasswd=conf.get('basic','dbpswd').strip("\"").strip("\'")
        self.conn = MySQLdb.Connect( user=confuser, passwd=confpasswd, db=confdb,charset='utf8')
        self.cursor=self.conn.cursor() 


        self.crawldate=time.strftime("%Y-%m-%d",time.localtime())


    def process_item(self, item, spider):
        if len(item)==0:
            return item
        itemcls=item.__class__.__name__
        itemlevel=int(re.search("level(\d+)",itemcls).group(1))
        itemdef=re.search("level\d+(item\d+)",itemcls).group(1)
        if itemdef in spider.sin_targets_xpath[itemlevel]:
            self.store_sin_item(spider,item,itemlevel,itemdef)
        elif itemdef in spider.mul_targets_xpath[itemlevel]:
            self.store_mul_item(spider,item,itemlevel,itemdef)
        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()
        spider.browser.close()
        print "finish!"

    def store_mul_item(self,spider,item,itemlevel,itemdef):
        #Note that the keys method return the keys without ensuring the order. But if we use itemnames with determined order consistently, the order problem will be solved.
        itemnames=spider.mul_targets_xpath[itemlevel][itemdef].keys()
        #Note that [] gets a list but () gets a generator
        itemtuple=(item[itemname] for itemname in itemnames)
        itemlist=zip(*itemtuple)
        suffix=""
        if itemdef in self.suffix[itemlevel]:
                suffix=item[self.suffix[itemlevel][itemdef]][0]

        for instance in itemlist:
            #Use 'insert ignore' to handle duplicate items
            querystring="insert ignore into `"+self.prefix[itemlevel][itemdef]+suffix+"`("+','.join(itemnames)+") value ("+','.join(("\'%s\'",)*len(itemnames))+")"
            
            querystring=querystring % instance
            self.cursor.execute(querystring)
        self.conn.commit()


    def store_sin_item(self,spider,item,itemlevel,itemdef):
        itemnames=spider.sin_targets_xpath[itemlevel][itemdef].keys()
        #Note that [] gets a list but () gets a generator
        instance=[item[itemname] for itemname in itemnames]
        suffix=""
        if itemdef in self.suffix[itemlevel]:
            suffix=item[self.suffix[itemlevel][itemdef]]

        querystring="insert ignore into `"+self.prefix[itemlevel][itemdef]+suffix+"`("+','.join(itemnames)+") value ("+','.join(("\'%s\'",)*len(itemnames))+")" 
        querystring=querystring % tuple(instance)
        self.cursor.execute(querystring)
        self.conn.commit()


