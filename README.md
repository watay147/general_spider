# general_spider
## Introduction
  The goal to develop this spider is to help crawler developers to crawl most websites without heavily coding (only offer some functions on how to extract data properly). By just configuring, one can use this spider to crawl most websites with ajax but get rid of analysing the ajax process. More features and weakness are listed below. Strongly recommend you to read through them before using this spider.  
  If you find this spider helpful, a star is undoubtedly a wonderful gift to me! And any problems with this spider are welcome and feel free to post them on issue of this project.

## Feature
- After some configuring, you can use this spider to crawl most websites without heavily coding (only offer some functions on how to extract data properly), except those pages that need a click or other mouse event to generate infomation within the same page (feel free if the mouse event get another page containing the target infomation, since another page just cause level+1 which is a normal situation this spider can handle). And it is reatively convenient to configure.
- The spider is based on scrapy project (http://scrapy.org/), which means you can enjoy some helpful features (like fast network processing using twisted library and multi-thread) which had been provided by scrapy.
- For generality, the spider is designed to crawl pages in infinite depth. That is, you can start crawling from page A (supposed it is in level 0), and then crawl page B got from page A (i.e. B is in level 1), and page C from D, and so on without limit of depth. 
- With configuration, this spider can crawl pages where some target infomation is generated by ajax (without an extra mouse event). This can help the developer to avoid analysing the ajax process of the website. To implement this, firefox browser (supposed had been installed) is called through selenium library(http://www.seleniumhq.org/). Therefore, by configuring, things you can see when you open the page by the browser is also seeable to this spider theoretically. Indeed, we can call firefox everytime for crawling, but for some page without ajax, the cost of calling browser is unbearable. So users can use configuration to determine in which page the browser should be used.
- You can offer your own extracting functions or just use functions had been written to extract and process data properly. For example, a date on the page is "2015/05/22" and you can write your own functions with re library to extract "2015","05" and "22", respectively.
- After creating tables in the database you want to store the data in previously, you don't have to think about how to code to store data into proper table with proper field name. The configuration will help you complete all these with few effort. Indeed, you can curstomize which table your data will be stored in and whether data should be stored into different tables depends one of its value or not. However, note that for V0.1 the database software is limited to be MySQL.
- Log is provided to record note of page crawled in level 0 for reference when you have to restart the spider.
- If the browser raise exception when crawling a page, this page will be crawled again if the exception can be handled. However, this won't work for some situations. For example, your IP had been banned by the website. For this situation, spider may crash or just look like pausing. You should stop the spider if needed and check the problem. And then, use the log for reference to restart the spider at the right point (by configuring the url for starting to crawl).



## Weakness
- As have been dicussed, this spider can not use to crawl pages that need a click or other mouse event to generate infomation within the same page. Unfortunately, you have to turn to other tools or code by yourself in this case.
- Since for now the browser used is firefox, which requires GUI interface, OS without GUI can not use this spider. Windowless browser like HTMLUNIT had been tried, but the reliability of it is not as sufficient as firefox (i.e. HTMLUNIT is more likely to crash or miss elements). You can customize this if you have to run this spider in an OS without GUI. Read the notes of the general_spider.py for details.
- The spider assume every level contains only one page (but you can edit different working configuring files for each route respectively). See more in notes of the config.py.
- More customizability like changing the database software for storing data, changing browser for calling is waiting for implement.

## Installation & Usage
- Installation
  + Scrapy and selenium library are needed for this spider, you should install them first.  
    ```pip install scrapy```  
    ```pip install selenium```
  + If the page crawled has some element generated by ajax, firefox(http://www.firefox.com) browser should be installed before. And then, you should make sure that path to firefox's executable file had been properly appended to the environment variable "path".
  + Directly clone this project to anywhere you want to do your crawling. Like:  
  ```git clone urlOfThisProject```
- Usage
  + After finishing installation stegs listed above, turn to the folder you clone this project to.
  + Type  
  ```python manage.py -gencfg n path```  
    to generate working configuring file template for n levels crawling and store it at where the path parameter point out.
  + Edit the generated working configuring file based on the guide of the config.py, and 
  + Type  
  ```python manage.py -run```  
    to run the spider.
- You can turn to the example folder to use the demo configuring file to run. Read the readme.md at that fodler first.


