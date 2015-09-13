#encoding=utf-8
#########V0.3使用和扩展简介##############################
#   首先安装scrapy和selenium,安装方法为先安装pip包管理工具，再使用pip命令进行安装：
#   pip install scrapy和pip install selenium
#   配置修改完后，先通过命令行启动htmlunit(selenium server的jar包里已经包含)，在selenium-server-standalone-2.40.0.jar所在目录下执行java -jar selenium-server-standalone-2.40.0.jar,然后在本.py文件存放路径下命令行执行scrapy runspider general_spider.py即可。
#注：selenium-server-standalone-2.40.0.jar的启动可以传递一个port参数如：
#java -jar selenium-server-standalone-2.40.0.jar -port 4445
#来指定端口号，未指定时默认是4444，selenium.webdriver.remote方法建立连接时默认也是连接4444端口，如果需要在一台机器上启动多个实例，需要以不同端口号启动多个实例，此时在python代码里调用remote方法时传入相应的command_executor参数接口，如4445端口：
#browsers= webdriver.Remote(command_executor="http://127.0.0.1:4445/wd/hub",desired_capabilities=DesiredCapabilities.HTMLUNIT)
#
#
#   v0.2实现包括X，Y和Z三层，逻辑上Y页面的入口url由X页面产生,Z页面入口url由Y页面产生，每层页面支持Source设定入口url的xpath,支持爬取多重属性和单重属性，支持nextlink设置下一个同层页面的xpath。可以阅读代码后按照代码逻辑定义更多层级。
#   通过设置maxX可以控制测试时爬取的X层页面数目。
#配置和扩展注意事项：
#   1.配置上，在GeneralSpider类的开始定义要爬取的网页队列start_urls和爬取变量的xpath（标签请用小写字母表示），如：
#   start_urls = ['http://guba.eastmoney.com/list,000415.html']
#   Xtitle="//div[@class='articleh']/span[3]/a"
#   2.如果Y层入口url由Xtitle产生,则给出Ysource=Xtitle的声明。否则Ysource=""即可（程序会自动判断Ysource是否是空字符串），建议扩展更多层级时页参照这一编写方式。
#   每一层的下一页按钮请参照Xnextlink变量名定义，并可参照目前的实现方式进行实现。
#   3.给出xpath定义后，请修改funcDist字典，给出每个xpath获取到的元素的名称及对应预处理函数名（如果该函数是新增的请在辅助函数部分直接新写一个函数）。格式为：  属性名称:函数名
#   4.修改对应层的多重属性和单重属性元组列表，如XMulTarget和XSinTarget,*MulTarget用于存放多重属性，*SinTarget存放单重。加入的每个元组格式为：  (属性名称,xpath字符串变量名)
#   5.目前的实现中仅对Xnextlink进行是否需要动态获得（于是需要操控浏览器加载获得）的判断逻辑，对其他元素的获取如果需要这一判断逻辑也可以参考进行实现。
#   6.数据库的写入pipepiles.py里定义,建议先阅读这部分代码（并不长）,每层爬取的item定义在items.py里定义，数据项有变动时也需要修改。目前每一层使用sinitem(单个item)和mulitem（重复item）两种，mulitem放进来的方式是作为数组（deque）放入，最后再pipepiles里对多个数组按顺序解包从而保证属于同个文章的阅读数，标题等按顺序作为数据库的一行写入，具体可以看代码。
#   7.建议使用前先阅读完代码（并不长）。
#   8.运行过程中可能会在操控浏览器获取某个网页时卡住，可以检查下如果直接用浏览器访问是否会卡住，一般是因为网页某些ajax请求获取卡住了，可以检查是否需要开启外网等。self.browser.implicitly_wait(60)可以设置每次等待ajax多少秒（若60则等待60秒，提前拿到元素就继续，否则超时停止，参数可以自己调）
#   目前的速度：爬股吧170个文章2秒（用实验室爬虫是3秒/文章。。。）
#########################################################################
import os
import sys
import ConfigParser
import scrapy
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from collections import deque

from extracter import *
from general.items import *

class GeneralSpider(scrapy.Spider):
    name = 'general'
    start_urls = []
    



    def __init__(self):
        #Set up the connection to it and initinalize the browser.
        self.browser= webdriver.Remote("http://127.0.0.1:4800/wd/hub",desired_capabilities=DesiredCapabilities.HTMLUNIT)
        self.browser.implicitly_wait(60)
        self.max=2
        self.count=0


        #try to read the content from config files
        self.conf=ConfigParser.ConfigParser()
        conf=self.conf
        if not conf.read('config.py'):
            print "\'config.py\' not found, please make sure you have prepared such a file."
            sys.exit(1)
        confpath=conf.get('default','path')
        if not conf.read(confpath) :
            print "\'"+confpath+"\' not found, please make sure you have prepared such a file."

        self.start_urls=eval(conf.get('basic','urls'))
        self.levels=conf.get('basic','levels')
        self.func_dist=[]
        self.sin_targets_xpath=[]
        self.mul_targets_xpath=[]
        self.next_link=[]
        self.source_link=[]

        for index in range(int(self.levels)):
            self.func_dist.append({
                itemname : globals().get(funcname) 
                    for itemname,funcname in conf.items("level"+str(index)+"extract")})
            self.sin_targets_xpath.append({
                itemdef :  { itemname : conf.get("level"+str(index)+"xpath",itemname).strip("\"").strip("\'") for itemname in eval(itemlist) } 
                    for itemdef,itemlist in conf.items("level"+str(index)+"sinitems")})
            self.mul_targets_xpath.append({
                itemdef :  { itemname : conf.get("level"+str(index)+"xpath",itemname).strip("\"").strip("\'") for itemname in eval(itemlist) } 
                    for itemdef,itemlist in conf.items("level"+str(index)+"mulitems")})

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
        level=response.meta.get('level',0)
        if(level==0):
            self.count+=1
            if self.count>=self.max:
                return 


        #For single items, simply extract them into one pipeline object and yield it.
        for itemdef,xpaths in self.sin_targets_xpath[level].iteritems():
            pipeobj=globals().get("level"+str(level)+itemdef)()
            for itemname,xpath in xpaths.iteritems():
                itemcontent=self.func_dist[level][itemname](response.xpath(xpath).extract()[0])
                pipeobj[itemname]=itemcontent
            yield pipeobj

        #For multiple items, use deques to save the extracted items with different itemnames in order and yield the pipeline object containing such deques. Extra works should be done to handle these in pipelines.py.
        for itemdef,xpaths in self.mul_targets_xpath[level].iteritems():
            pipeobj=globals().get("level"+str(level)+itemdef)()
            for itemname,xpath in xpaths.iteritems():
                pipeobj[itemname]=deque()
                for item in response.xpath(xpath):
                    itemcontent=self.func_dist[level][itemname](item.extract())
                    pipeobj[itemname].append(itemcontent)
            yield pipeobj

        #Extract the source links to next level.
        if self.source_link[level]:
            for item in response.xpath(self.source_link[level]):
                full_url=response.urljoin(self.func_dist[level]['sourcelink'](item.extract()))
                yield scrapy.Request(full_url,callback=self.parse,meta={'level':level+1})

        #Extract the link to next page in the same level.
        if self.next_link[level]:
            nexthref=response.xpath(self.next_link[level])
            if nexthref:
                nexturl=self.func_dist[level]['nextlink'](nexthref.extract()[0])
                yield scrapy.Request(nexturl, callback=self.parse,meta={'level':level})
            #If failed, use browser to extract instead.
            else:
                self.browser.get(response.url)
                links=self.browser.find_elements_by_xpath(self.next_link[level])
                if links:
                    nexturl=links[0].get_attribute("href")
                    yield scrapy.Request(nexturl, callback=self.parse,meta={'level':level})

        
