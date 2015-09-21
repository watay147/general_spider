[basic]
urls=["http://guba.eastmoney.com/list,000415_810.html"]
levels=2
needbrowser=[0]
dbuser=root
dbpswd=
dbname=test

#Note: Do not use a name for item definition multiple times within a level. But this restrict doesn't matter for different levels.
[level0sinitems]


[level0mulitems]
item0=["title","articleid","stockno"]
item1=["reply","click"]

[level0dbprefix]
item0="update"
item1="update2"

[level0xpath]
stockno=""
title="//div[@class='articleh']/span[3]/a"
articleid="//div[@class='articleh']/span[3]/a/@href"
reply="//div[@class='articleh']/span[2]"
click="//div[@class='articleh']/span[1]"
nextlink="//span[@class='pagernums']/span/a[last()-1]"
sourcelink="//div[@class='articleh']/span[3]/a"

[level0extract]
stockno=extractstockno
title=extracttext
articleid=extracturlid
reply=extractint
click=extractint
nextlink=extracthref
sourcelink=extracthref


[level1sinitems]
item0=["title","content","author"]

[level1mulitems]


[level1dbprefix]
item0="update3"


[level1xpath]
title="//div[@id='zwconttbt']"
content="//div[@class='stockcodec']"
author="//div[@id='zwconttbn']/strong/*"

[level1extract]
content=extracttext
title=extracttext
author=extracttext