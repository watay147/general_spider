import os
import sys
import ConfigParser
import scrapy
import threading
import logging
import time
from selenium import webdriver


from collections import deque

from extracter import *


def gettime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

class GeneralSpider(scrapy.Spider):
    name = 'general'
    start_urls = []
    


    def __init__(self):
        #Set up the connection to it and initinalize the browser.
        #For V0.1, we assume that firefox had been installed and path to its executable file had been properly appended to the environment variable "path".
        #You can change the browser to HTMLUNIT if you want 
        self.browser=webdriver.Firefox()
        self.wait_sec=20
        self.browser.implicitly_wait(self.wait_sec)
        #20 seconds for the browser to wait for the element to be loaded is set by default, you can turn this depends on your network environment.

        #self.count is used for convenience in testing
        self.count=0

        

        
        #Note that the browser may be used in different threads concurrently, therefore a lock is required to make sure each thread extracts proper items. And thread locally safe variables are also needed.
        self.countmutex=threading.Lock()
        self.mutex=threading.Lock()
        self.thread_local=threading.local()

        #Try to read the content from config files.
        self.conf=ConfigParser.ConfigParser()
        conf=self.conf
        if not conf.read('config.py'):
            print "\'config.py\' not found, please make sure you have prepared such a file."
            sys.exit(1)
        confpath=conf.get('default','path')
        if not conf.read(confpath) :
            print "\'"+confpath+"\' not found, please make sure you have prepared such a file."
            sys.exit(1)

        #The log.txt will record the exceptions raised during crawling.
        self.ff=open('./log/'+os.path.basename(confpath)+'.log','w')

        self.start_urls=eval(conf.get('basic','urls'))
        self.levels=int(conf.get('basic','levels'))
        self.istest=int(conf.get('basic','test'))
        self.needbrowser=[False]*self.levels#browser is needless by default
        needbrowserlist=[]
        if(conf.has_option("basic",'needbrowser')):
            needbrowserlist=eval(conf.get('basic','needbrowser'))
        for level in needbrowserlist:
            self.needbrowser[int(level)]=True


        self.func_dist=[]
        self.sin_targets_xpath=[]
        self.mul_targets_xpath=[]
        self.next_link=[]
        self.source_link=[]
        self.item_classes={}

        for index in range(self.levels):
            #Fullfill function distionary for extracting different items.
            self.func_dist.append({
                itemname : globals().get(funcname) 
                    for itemname,funcname in conf.items("level"+str(index)+"extract")})
            #Fullfill single items' xpaths dictionary for different levels. 
            self.sin_targets_xpath.append({
                itemdef :  { itemname : conf.get("level"+str(index)+"xpath",itemname).strip("\"").strip("\'") for itemname in eval(itemlist) } 
                    for itemdef,itemlist in conf.items("level"+str(index)+"sinitemset")})
            #Fullfill multiple items' xpaths dictionary for different levels. 
            self.mul_targets_xpath.append({
                itemdef :  { itemname : conf.get("level"+str(index)+"xpath",itemname).strip("\"").strip("\'") for itemname in eval(itemlist) } 
                    for itemdef,itemlist in conf.items("level"+str(index)+"mulitemset")})

            #Dynamicaly create scrapy item classes.
            for itemdef,itemlist in conf.items("level"+str(index)+"sinitemset"):
                classname="level"+str(index)+itemdef
                itemlist=eval(itemlist)
                defdict={itemname:scrapy.Field() for itemname in itemlist}
                self.item_classes[classname]=type(classname,(scrapy.Item,),defdict)

            for itemdef,itemlist in conf.items("level"+str(index)+"mulitemset"):
                classname="level"+str(index)+itemdef
                itemlist=eval(itemlist)
                defdict={itemname:scrapy.Field() for itemname in itemlist}
                self.item_classes[classname]=type(classname,(scrapy.Item,),defdict)



            #Note that if we use [DEFAULT] to set the default value, them these key-value pairs will be return when you use 'items' method even if you set the sec argument for the section instead of DEFAULT. Therefore, before this rule being modified, we may just use has_option for expediency.
            if(conf.has_option("level"+str(index)+"xpath",'nextlink')):
                self.next_link.append(conf.get("level"+str(index)+"xpath",'nextlink').strip("\"").strip("\'"))
            else:
                self.next_link.append("")

            if(conf.has_option("level"+str(index)+"xpath",'sourcelink')):
                self.source_link.append(conf.get("level"+str(index)+"xpath",'sourcelink').strip("\"").strip("\'"))
            else:
                self.source_link.append("")


#The parser
    def parse(self, response):
        self.thread_local.level=response.meta.get('level',0)
        self.thread_local.shouldnext=True
        if(self.thread_local.level==0):
            with self.countmutex:
                self.count+=1
                #logging.debug(str(self.count)+','+response.url)
                self.ff.write('['+gettime()+'] '+response.url+'\n')
                self.ff.flush()
                if self.istest==1 and self.count>=3:
                    self.thread_local.shouldnext=False

        extract_by_xpath=None
        if self.needbrowser[self.thread_local.level]:
            self.mutex.acquire()
            try:
                self.browser.get(response.url)
                #Use browser.page_source method directly won't arouse implicit waiting, therefore find_elements_by_xpath should be use previously to make sure the browser has wait until timeout or got the element.

                #TODO: There may be a problem here: the browser query on a xpath for multiple items, but maybe only one of a part items have arrived instead of all the items, in this case the page_source would be incomplete so that extraction won't be complete, too.This problem lets me to use response.xpath for some extractions temporarily.....
                

                for itemdef,xpaths in self.sin_targets_xpath[self.thread_local.level].iteritems():
                    for itemname,xpath in xpaths.iteritems():
                        if xpath:
                            a=xpath.find('/@')
                            if a==-1:
                                a=len(xpath)
                            self.browser.find_elements_by_xpath(xpath[:a])
                for itemdef,xpaths in self.mul_targets_xpath[self.thread_local.level].iteritems():
                    for itemname,xpath in xpaths.iteritems():
                        if xpath:
                            a=xpath.find('/@')
                            if a==-1:
                                a=len(xpath)
                            self.browser.find_elements_by_xpath(xpath[:a])
                if self.source_link[self.thread_local.level]:
                    self.browser.find_elements_by_xpath(self.source_link[self.thread_local.level])

                if self.next_link[self.thread_local.level]:
                    self.browser.find_elements_by_xpath(self.next_link[self.thread_local.level])
                #Take advantages of scrapy's selector to provide the same APIs for extraction.
                sel=scrapy.Selector(text=self.browser.page_source)
                extract_by_xpath=sel.xpath
            except Exception,e:
                self.browser.close()
                self.browser=webdriver.Firefox()
                self.browser.implicitly_wait(self.wait_sec)
                yield scrapy.Request(response.url, callback=self.parse,meta={'level':self.thread_local.level})
            finally:
                self.mutex.release()
        else:
            extract_by_xpath=response.xpath




        #For single items, simply extract them into one pipeline object and yield it.
        for itemdef,xpaths in self.sin_targets_xpath[self.thread_local.level].iteritems():
            pipeobj=self.item_classes.get("level"+str(self.thread_local.level)+itemdef)()
            for itemname,xpath in xpaths.iteritems():
                if xpath:
                    itemcontent=self.func_dist[self.thread_local.level][itemname](response.xpath(xpath).extract()[0])
                else:
                #Note: an empty xpath means extract the current url.
                    itemcontent=self.func_dist[self.thread_local.level][itemname](response.url)
                pipeobj[itemname]=itemcontent
            yield pipeobj

        #For multiple items, use deques to save the extracted items with different itemnames in order and yield the pipeline object containing such deques. Extra works should be done to handle these in pipelines.py.
        for itemdef,xpaths in self.mul_targets_xpath[self.thread_local.level].iteritems():
            pipeobj=self.item_classes.get("level"+str(self.thread_local.level)+itemdef)()
            urlextract=deque()#Store all the item names extracted by url.
            xpathextract=""#Store any one item name extracted by xpath.
            for itemname,xpath in xpaths.iteritems():
                if xpath:
                    xpathextract=itemname
                    pipeobj[itemname]=deque()
                    for item in response.xpath(xpath):
                        itemcontent=self.func_dist[self.thread_local.level][itemname](item.extract())
                        pipeobj[itemname].append(itemcontent)
                else:
                #Note: an empty xpath means extract the current url. And since item extract from url is single, extra process is needed to transform it to be multiple.
                    pipeobj[itemname]=[None]#Use list because of the convenience like [1]*2 makes [1,1]
                    pipeobj[itemname][0]=self.func_dist[self.thread_local.level][itemname](response.url)
                    urlextract.append(itemname)
            if xpathextract:
                #If no any items extracted by xpath, then the transformation is needless.
                for itemname in urlextract:
                    pipeobj[itemname]=pipeobj[itemname]*len(pipeobj[xpathextract])
            yield pipeobj


        #Extract the source links to next level.
        if self.source_link[self.thread_local.level]:
            i=0
            for item in response.xpath(self.source_link[self.thread_local.level]):
                i+=1
                full_url=response.urljoin(self.func_dist[self.thread_local.level]['sourcelink'](item.extract()))
                yield scrapy.Request(full_url,callback=self.parse,meta={'level':self.thread_local.level+1})
            self.ff.write(str(i)+'\n')
            self.ff.flush()

        #Extract the link to next page in the same level.
        if self.thread_local.shouldnext and self.next_link[self.thread_local.level]:
            nexthref=extract_by_xpath(self.next_link[self.thread_local.level])
            if nexthref:
                nexturl=response.urljoin(self.func_dist[self.thread_local.level]['nextlink'](nexthref.extract()[0]))
                yield scrapy.Request(nexturl, callback=self.parse,meta={'level':self.thread_local.level})

        
