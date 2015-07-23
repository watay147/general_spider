import os
import re

pagessum=[
744,
397,
232,
273,
775,
604,
148,
425,
177,
150,
527,
202,
122,
625,
195,
206,
293,
127,
183,
103,
970,
230,
1396,
448,
312,
251,
249,
463,
1609,
355,
383,
794,
939,
338,
398,
312,
440,
146,
199
]

tarwebsites=[
"http://guba.eastmoney.com/list,000415_1.html",
"http://guba.eastmoney.com/list,002256_1.html",
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
]
for index,i in enumerate(tarwebsites):
    f=open('start.txt','w')
    f.write(i)
    f.close()
    while  True:
        os.system("scrapy crawl general")
        f=open("test.txt")
        l=f.readlines()
        f.close()
        total=pagessum[index]
        res=re.search(r'_\d+',l[-1])
        if res:
            last=int(res.group(0)[1:])
            if last>=total:
        	    break        
            f=open('start.txt','w')
            f.write(l[-1][:-1])
            f.close()
        else:
            break



print "rerun finish"