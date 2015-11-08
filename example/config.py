#The name of this file can not be changed!
#This file configure the path to the working configuring file.
#
#To work, a 'default' section is required. Edit this file like
#[default]
#path= path to the working configuring file
#
#You can turn to the 'example' folder where the example file
#may bring you more helpful infomation.
[default]
path=./example/forumnconfig.py



#To set the working configuring file properly, we should 
#first know some kind of mechanism about how this spider works.
#
#Supposed that the target pages in website lie in different levels 
#The spider assume the start point of these pages to be level 0, 
#and every level contains only one page (this maybe a 
#limit of this spider but you can edit different working 
#configuring files for each route respectively).
#
#For each level, the stragety for using browser or not is the 
#same (since the cost of calling the browser will be spent even 
#though only one element crawled in this page need it).
#
#For each level/page, you can crawl several item sets and each set 
#contains several items. An item set is a unit for storing data 
#into the database (i.e. storing into the same table) and an item 
#is the unit of information crawled (i.e. target element of pages)
#from the page. There are two kinds of item sets by definition, 
#one for single items (i.e. these items appear once per page) and 
#the other for multiple items (i.e. appear multiple times per page)
#. You can combine any items to make any item sets, but appearing 
#times of items within an item set should be the same.
#
#All things needed for crawling an item is just its xpath within #the page.
#
#
#Note: each configuration should be written within a line! (This 
#is because ConfigParser class is used for loading configuraton.)
#Each configuration is look like: key=value
#
#For the working configuring file, a 'basic' section is 
#necessary and other sections depends on the number of levels 
#of the pages crawled are required, too.
#
#For the 'basic' section:
#1. set urls, which should be a list of urls for the start 
#points for crawling.
#2. set levels, which should be the number of level for the 
#deepest page crawled. It should be a number.
#3. set test, 1 means test for no more than crawling 3 
#pages, other number such as 0 means formally crawling.
#4. set needbrowser, which should be a list of indexes of 
#level where browser should be used for crawling (i.e. at 
#least one of the target elements in this level is generated 
#by ajax).
#5. set dbuser, which should be the account for storing data 
#into your database. In V1.0, the mysql database is required. 
#Note that no any quote is needed.
#5. set dbpswd, which should be the password for the account 
#above. Note that no any quote is needed.
#6. set dbname, which should be the name of the base you want #to store in your database software.
#
#Then, another n*6 sections are required where n is the 
#number of level you set before. In V1.0, a working 
#configuring file generator hadn't been coded, but it will be 
#provided in the future.
#
#Each section name starts with a prefix of 'levelx', where x 
#is the number of the level this section are configuring.
#
#For each level, 6 sections are required. 
#
#levelxsinitemset section:
#This section declare the item sets containing single items. Each 
#declaration consists of a item set name and a list containing the 
#items' names (which will be defined in levelxxpath section). The 
#names of item sets can not be duplicate within a level, but no 
#similar limit for different levels.
#
#levelxmulitemset section:
#This section declare the item sets containing multiple items. 
#Each declaration consists of a item set name and a list 
#containing the items' names.
#
#levelxdbprefix:
#This section declare prefix of table names in database the item 
#sets will be stored. You can use these prefix to make sure which 
#table each item set will be stored. For example, item0="t1" means 
#that data in item set item0 will be store into table whose name #starts with "t1". Note that the quotes will not be used indeed.
#
#levelxdbsuffix:
#This section declare suffix of table names in database the item 
#sets will be stored. But the goal of suffix is not the same with 
#the prefix. Each suffix consists of an item name. When storing, 
#value of this item crawled will be use as the actual suffix of 
#the name of the table stored. This design, for example, will help 
#you to store things into different tables depending on any id or 
#date you crawled from the page.
#
#levelxxpath:
#This section declare xpath to get the items in page. Each 
#declaration consists of item name and the xpath of this item. 
#Note that there are two special item names (or you can call them 
#reserved words) of this spider, "nextlink" and "sourcelink". 
#"nextlink" item is used to get the link to next page of the same 
#level. And "sourcelink" item is used to get the link to the page 
#in deeper level (i.e. in oldlevel+1 level). If no next page in 
#the same level or no page in next level wanted, just don't set 
#them. The names of items can not be duplicate within a level, but 
#no similar limit for different levels.
#
#levelxextract:
#This section declare extracting functions for extract and process 
#data properly per item. Each declaration consists of item name 
#and the name of function used as extracter. Extracting functions 
#should be written in ./general/spiders/extracter.py. Some 
#extracters had been written for your convenience, but you can 
#also write your own if needed and use them by declaring here.
#
#You can turn to the 'example' folder where the example file
#may bring you more helpful infomation.

