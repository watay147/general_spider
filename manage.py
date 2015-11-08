#encoding:utf8
import sys
import os




def run_spider():
    if not os.path.exists(r"./log/"):
        os.mkdir(r"./log/")
    os.system("scrapy crawl general")

def genconfig():
    levels=int(sys.argv[2])
    with open(sys.argv[3],'w') as f:
        basic=("[basic]\n"+
        "urls=[]\n"+
        "levels=%d\n" % (levels,)+
        "needbrowser=[]\n"+
        "test=\n"+
        "dbuser=\n"+
        "dbpswd=\n"+
        "dbname=\n\n")
        f.write(basic)
        for i in range(levels):
            string="[level%dsinitemset]\n\n\n[level%dmulitemset]\n\n\n[level%ddbprefix]\n\n\n[level%ddbsuffix]\n\n\n[level%dxpath]\n\n\n[level%dextract]\n\n\n" % ((i,)*6)
            f.write(string)



if __name__ == "__main__":
    if sys.argv[1]=='-h':
        print "Help Info:\n\t\'python manage.py -run\' to run the spider.\n\t\'python manage.py -gencfg n path\' to generate working configuring file\n\ttemplate for n levels crawling and store it at where the path parameter\n\tpoint out."

    elif sys.argv[1]=='-run':
        run_spider()
    elif sys.argv[1]=='-gencfg':
        genconfig()

