#encoding=utf-8
#########V0.1使用和扩展简介##############################
#	首先安装scrapy和marionette,安装方法为先安装pip包管理工具，再使用pip命令进行安装：
#	pip install scrapy和pip install marionette_client
#	配置修改完后，先通过命令行执行firefox -marionette命令启动firefox（或者windows下通过设置快捷方式对应属性来启动），然后在该文件存放路径下命令行执行scrapy runspider general_spider.py即可
#	目前的实现分为X和Y两层，逻辑上Y页面的入口url由X页面产生，可以阅读代码后按照代码逻辑定义更多层级。
#	通过设置maxX可以控制测试时爬取的X层页面数目。
#配置和扩展注意事项：
#	1.配置上，在GeneralSpider类的开始定义要爬取的网页队列start_urls和爬取变量的xpath（标签请用小写字母表示），如：
#	start_urls = ['http://guba.eastmoney.com/list,000415.html']
#	Xtitle="//div[@class='articleh']/span[3]/a"
#	2.如果Y层入口url由Xtitle产生,则给出Ysource=Xtitle的声明。否则Ysource=""即可（程序会自动判断Ysource是否是空字符串），建议扩展更多层级时页参照这一编写方式。
#	每一层的下一页按钮请参照Xnextlink变量名定义，并可参照目前的实现方式进行实现。
#	3.给出xpath定义后，请修改funcDist字典，给出每个xpath获取到的元素的名称及对应预处理函数名（如果该函数是新增的请在辅助函数部分直接新写一个函数）。格式为	属性名称:函数名
#	4.修改对应层的多重属性和单重属性元组列表，如XMulTarget和XSinTarget,*MulTarget用于存放多重属性，*SinTarget存放单重。加入的每个元组格式为	(属性名称,xpath字符串变量名)
#	5.目前的实现中仅对Xnextlink进行是否需要动态获得（于是需要marionette来操控浏览器加载获得）的判断逻辑，对其他元素的获取如果需要这一判断逻辑也可以参考加上。
#	6.目前的测试中爬取到的内容会输出到控制台并以utf8编码写入到当前路径下的test.txt文件（阅读代码可以获悉），由于没有使用完整的scrapy框架（完整爬虫项目除spider文件外还需定义settings.py,pipepiles.py等），没有合适的位置来关闭打开的文本文件（可能在某处关闭后其他线程还没有结束，会造成对已关闭文件的写入），故写入时都使用了flush方法来刷新写缓冲区以保证跑完时得到的输出文件内容完整。这些问题会在后续使用完整框架时解决。
#	7.建议使用前先阅读完代码（并不长）。
#	8.运行过程中可能会在使用marionette获取某个网页时卡住，可以检查下如果直接用浏览器访问是否会卡住，一般是因为网页某些ajax请求获取卡住了，可以检查是否需要开启外网等。
#	目前的速度：爬股吧170个文章2秒（用实验室爬虫是3秒/文章。。。）
#	9.使用project形式组织的话，每次修改需要修改spider,items,pipelines，	##################################################################

import scrapy
import os
from collections import deque
from marionette import Marionette
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
from general.items import XMulItem
from general.items import XSinItem
from general.items import YMulItem
from general.items import YSinItem
from general.items import ZMulItem
from general.items import ZSinItem
class GeneralSpider(scrapy.Spider):
    name = 'general'
    start_urls = ['http://guba.eastmoney.com/list,000415.html']
    maxX=1#控制测试时爬取的X层页面数目。
    countX=0
    Xtitle="//div[@class='articleh']/span[3]/a"
    Xauthor="//div[@class='articleh']/span[4]/*[1]"
    Xreply="//div[@class='articleh']/span[2]"
    Xclick="//div[@class='articleh']/span[1]"
    Xnextlink="//span[@class='pagernums']/span/a[last()-1]"
    Ysource=Xtitle
    Ycontent="//*[@id='zwconbody']/div"
    Ydate="//div[@id='zwconttb']/div[2]"
    YcommentAuthor="//div[@class='zwlianame']/span/a"
    YcommentDate="//div[@class='zwlitime']"
    YcommentContent="//div[@class='zwlitx']/div/div[3]"
    Zsource="//*[@id='newspage']/span/a[last()-1]"
    Znextlink=Zsource
    ZcommentAuthor="//div[@class='zwlianame']/span/a"
    ZcommentDate="//div[@class='zwlitime']"
    ZcommentContent="//div[@class='zwlitx']/div/div[3]"



    def __init__(self):
        #启动Marionette的client并链接firefox
        self.client = Marionette('localhost', port=2828)
        self.client.start_session()
	#self.browser = webdriver.Remote(desired_capabilities=DesiredCapabilities.HTMLUNIT)
	self.f=open('test.txt','w')#用于存储测试输出内容的文本文件
	#每项的预处理函数字典
	self.funcDist={
		'Xtitle':self.extracttext,
		'Xauthor':self.extracttext,
		'Xreply':self.extractint,
		'Xclick':self.extractint,
		'Ycontent':self.extracttext,	
		'Ydate':self.extracttime,
		'YcommentAuthor':self.extracttext,
		'YcommentDate':self.extracttime,
		'YcommentContent':self.extracttext,
		'ZcommentAuthor':self.extracttext,
		'ZcommentDate':self.extracttime,
		'ZcommentContent':self.extracttext,
		}
	#每项的名称与对应xpath元组，名称将用于索引预处理函数和作为数据库的键值，由于是字典，所以各层的类似元素名称必须不一样，考虑到可能不希望数据库的键值带有X，后面pipepiles.py可以取[1:]部分
	self.XMulTarget=[
			('Xtitle',self.Xtitle),	
			('Xauthor',self.Xauthor),
			('Xreply',self.Xreply),
			('Xclick',self.Xclick)
		]
	self.XSinTarget=[]
	self.YMulTarget=[
			('YcommentAuthor',self.YcommentAuthor),
			('YcommentDate',self.YcommentDate),
			('YcommentContent',self.YcommentContent)
			]
	self.YSinTarget=[
			('Ycontent',self.Ycontent),
			('Ydate',self.Ydate)
		]
        self.ZMulTarget=[
			('ZcommentAuthor',self.YcommentAuthor),
			('ZcommentDate',self.YcommentDate),
			('ZcommentContent',self.YcommentContent)
			]
        self.ZSinTarget=[
			]
    def end(self):
            self.client.delete_session()
            
            print "finish!"

#######辅助函数#######
	
    #用于取出元素内部的文本内容
    def extracttext(self,s):
        res=re.search(">.*<",s)
        if res:
            return res.group(0)[1:-1].strip()
        return ""

    #用于取出href属性内容
    def extracthref(self,s):
        res=re.search('''href=\"[^"]+"''',s)
        if res:
            return res.group(0)[6:-1].strip()
        return ""

    #用于取出元素内部的xxxx-xx-xx xx:xx:xx格式的时间内容
    def extracttime(self,s):
        s=self.extracttext(s)
        if s:
           res=re.search(r'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d',s)
           if res:
               return res.group(0)
        return ""
    #取出整数部分
    def extractint(self,s):
        s=self.extracttext(s)
        if s:
           res=re.search(r'\d+',s)
           if res:
               return res.group(0)
        return ""
        
#######辅助函数#######


######X层工作函数
    def parse(self, response):
        #控制爬取的X页数目
        self.countX+=1
        if self.countX>self.maxX:
            self.end()
            return
        #爬取X页的多重属性
        Xmuls=XMulItem()
        for name,target in self.XMulTarget:
            Xmuls[name]=deque()
            for item in response.xpath(target):
                itemcontent=self.funcDist[name](item.extract())
                Xmuls[name].append(itemcontent)
                print itemcontent
                self.f.write(itemcontent.encode('utf8')+'\n')
                self.f.flush()
        yield Xmuls
        #爬取X页的单重属性
        Xsin=XSinItem()
        for name,target in self.XSinTarget:
            itemcontent=self.funcDist[name](response.xpath(target).extract()[0])
            Xsin[name]=itemcontent
            print itemcontent
            self.f.write(itemcontent.encode('utf8')+'\n')
            self.f.flush()
        yield Xsin
        #产生到Y页的链接
        if self.Ysource:
            for item in response.xpath(self.Ysource):
                full_url=response.urljoin(self.extracthref(item.extract()))
                yield scrapy.Request(full_url, callback=self.parse_Y)
        nexthref=response.xpath(self.Xnextlink)
        #构造到下一个同层页的链接
        if nexthref:
            nexturl=self.extracthref(nexthref.extract()[0])
            yield scrapy.Request(nexturl, callback=self.parse)
        #如果获取不到，说明要获取的元素是动态得到的，应该使用Marionette来获取。
        else:
            print "Marionette操控浏览器访问url:"+response.url
            self.client.navigate(response.url)#访问当前访问的网址
            links=self.client.find_elements('xpath',self.Xnextlink)#使用同样的xpath获取元素
            print links[0].get_attribute("href")
            if links:
                nexturl=links[0].get_attribute("href")
                yield scrapy.Request(nexturl, callback=self.parse)
            else:
                print "end!"

######Y层工作函数
    def parse_Y(self, response):
        for name,target in self.YMulTarget:
            for item in response.xpath(target):
                itemcontent=self.funcDist[name](item.extract())
                #print itemcontent
                self.f.write(itemcontent.encode('utf8')+'\n')
                self.f.flush()
        for name,target in self.YSinTarget:
            itemcontent=self.funcDist[name](response.xpath(target).extract()[0])
            #print itemcontent
            self.f.write(itemcontent.encode('utf8')+'\n')
            self.f.flush()
        #产生到Z页的链接
        if self.Zsource:
            for item in response.xpath(self.Zsource):
                if item:
                    full_url=response.urljoin(self.extracthref(item.extract()))
                    yield scrapy.Request(full_url, callback=self.parse_Z)
                else:
                    print "Marionette操控浏览器访问url:"+response.url
                    self.client.navigate(response.url)#访问当前访问的网址
		    links=self.client.find_elements('xpath',self.Xnextlink)#使用同样的xpath获取元素
                    for taga in links:
                        href=taga.get_attribute("href")
                        yield scrapy.Request(href, callback=self.parse_Z)
                    break

######Z层工作函数
    def parse_Z(self, response):
        #爬取Z页的多重属性
        for name,target in self.ZMulTarget:
            for item in response.xpath(target):
                itemcontent=self.funcDist[name](item.extract())
                #print itemcontent
                self.f.write(itemcontent.encode('utf8')+'\n')
                self.f.flush()
        #爬取Z页的单重属性
        for name,target in self.ZSinTarget:
            itemcontent=self.funcDist[name](response.xpath(target).extract()[0])
            #print itemcontent
            self.f.write(itemcontent.encode('utf8')+'\n')
            self.f.flush()
        #构造到下一个同层页的链接
        nexthref=response.xpath(self.Znextlink)     
        if nexthref:
            nexturl=self.extracthref(nexthref.extract()[0])
            yield scrapy.Request(nexturl, callback=self.parse_Z)
        #如果获取不到，说明要获取的元素是动态得到的，应该使用Marionette来获取。
        else:
            print "Marionette操控浏览器访问url:"+response.url
            self.client.navigate(response.url)#访问当前访问的网址
            links=self.client.find_elements('xpath',self.Xnextlink)#使用同样的xpath获取元素
            print links[0].get_attribute("href")
            if links:
                nexturl=links[0].get_attribute("href")
                yield scrapy.Request(nexturl, callback=self.parse_Z)
            else:
                print "end!"
