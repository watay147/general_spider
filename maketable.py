import MySQLdb
import pandas as pd
import re
conn = MySQLdb.Connect( user='root',  db='guba',charset='utf8')
cursor=conn.cursor()
l=["http://guba.eastmoney.com/list,000415_1.html",
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
for i in l:
    num=re.search(r',\d+',i).group(0)[1:]
    cursor.execute("CREATE TABLE IF NOT EXISTS `reply%s` (`commentAuthor` varchar(40) NOT NULL,`commentDate` datetime NOT NULL,`commentContent` varchar(500) NOT NULL,`commentAuthorid` bigint(64) NOT NULL,`articleid` int(64) NOT NULL,UNIQUE KEY `uk_t_1` (`commentAuthorid`,`commentDate`)) ENGINE=InnoDB DEFAULT CHARSET=utf8; "% (num,))
    cursor.execute('''CREATE TABLE IF NOT EXISTS `gubarticleupdate%s` (
  `title` varchar(100) NOT NULL,
  `articleid` int(40) NOT NULL,
  `stockno` char(10) NOT NULL,
  `reply` int(11) NOT NULL,
  `click` int(11) NOT NULL,
  `crawldate` date NOT NULL,
  UNIQUE KEY `uk_t_1` (`crawldate`,`articleid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;'''% (num,))
    cursor.execute('''CREATE TABLE IF NOT EXISTS `article%s` (
  `title` varchar(100) NOT NULL,
  `articleid` int(40) NOT NULL,
  `stockno` char(10) NOT NULL,
  `content` text NOT NULL,
  `author` varchar(40) NOT NULL,
  `time` datetime NOT NULL,
  UNIQUE KEY `articleid` (`articleid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;'''% (num,))
    conn.commit()
cursor.close()
conn.close()
