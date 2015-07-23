from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
browser= webdriver.Remote(desired_capabilities=DesiredCapabilities.HTMLUNIT)
browser.implicitly_wait(60)
l=["http://guba.eastmoney.com/list,000415_1.html",
"http://guba.eastmoney.com/list,300207_1.html",
"http://guba.eastmoney.com/list,300015_1.html",
"http://guba.eastmoney.com/list,600257_1.html",
"http://guba.eastmoney.com/list,002183_1.html",
"http://guba.eastmoney.com/list,002425_1.html",
"http://guba.eastmoney.com/list,000534_1.html",
"http://guba.eastmoney.com/list,002711_1.html",
"http://guba.eastmoney.com/list,300030_1.html",
"http://guba.eastmoney.com/list,002130_1.html",
"http://guba.eastmoney.com/list,002388_1.html",
"http://guba.eastmoney.com/list,300167_1.html",
"http://guba.eastmoney.com/list,600588_1.html",
"http://guba.eastmoney.com/list,002551_1.html",
"http://guba.eastmoney.com/list,002210_1.html",
"http://guba.eastmoney.com/list,002249_1.html",
"http://guba.eastmoney.com/list,300277_1.html",
"http://guba.eastmoney.com/list,300090_1.html",
"http://guba.eastmoney.com/list,002620_1.html",
"http://guba.eastmoney.com/list,000039_1.html",
"http://guba.eastmoney.com/list,000035_1.html",
"http://guba.eastmoney.com/list,600518_1.html",
"http://guba.eastmoney.com/list,600577_1.html",
"http://guba.eastmoney.com/list,002416_1.html",
"http://guba.eastmoney.com/list,002583_1.html",
"http://guba.eastmoney.com/list,002684_1.html",
"http://guba.eastmoney.com/list,300088_1.html",
"http://guba.eastmoney.com/list,600567_1.html",
"http://guba.eastmoney.com/list,002640_1.html",
"http://guba.eastmoney.com/list,600446_1.html",
"http://guba.eastmoney.com/list,600978_1.html",
"http://guba.eastmoney.com/list,600696_1.html",
"http://guba.eastmoney.com/list,002325_1.html",
"http://guba.eastmoney.com/list,002334_1.html",
"http://guba.eastmoney.com/list,002535_1.html",
"http://guba.eastmoney.com/list,000837_1.html",
"http://guba.eastmoney.com/list,300348_1.html",
"http://guba.eastmoney.com/list,300301_1.html"]
pagessum=[]
for i in l:
	browser.get(i)
	pagessum.append(int(browser.find_element_by_xpath("//span[@class='sumpage']").text))

for i in l:
	browser.get(i)
	print browser.find_element_by_xpath("//span[@class='sumpage']").text+','

