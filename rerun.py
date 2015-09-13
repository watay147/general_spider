import os
import re

pagessum=[
760,
405,
235,
275,
786,
609,
149,
435,
180,
153,
530,
203,
123,
655,
198,
207,
302,
128,
185,
103
]

tarwebsites=[
"http://guba.eastmoney.com/list,000415_1.html",
"http://guba.eastmoney.com/list,002256.html",
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

]
pagessum=[
900,
400,
450,
80,
120,
1700,
400,
2500,
210,
171,
266,
351,
2541,
4440
]
tarwebsites=[
"http://guba.eastmoney.com/list,300059,f_1.html",
"http://guba.eastmoney.com/list,600151,f_1.html",
"http://guba.eastmoney.com/list,000547,f_1.html",
"http://guba.eastmoney.com/list,002508,f_1.html",
"http://guba.eastmoney.com/list,002042,f_1.html",
"http://guba.eastmoney.com/list,601668,f_1.html",
"http://guba.eastmoney.com/list,002456,f_1.html",
"http://guba.eastmoney.com/list,600030,f_1.html",
"http://guba.eastmoney.com/list,300364,f_1.html",
"http://guba.eastmoney.com/list,300380,f_1.html",
"http://guba.eastmoney.com/list,300274,f_1.html",
"http://guba.eastmoney.com/list,300056,f_1.html",
"http://guba.eastmoney.com/list,601988,f_1.html",
"http://guba.eastmoney.com/list,601857,f_1.html",
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