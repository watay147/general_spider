#encoding:utf8
import re
#######辅助函数#######
    
    #用于取出元素内部的文本内容
def extracttext(s):
    res=re.search(">.*<",s,re.DOTALL)
    if res:
        ans=res.group(0)[1:-1].strip()
        ans=re.sub(r'<[^>]*>','',ans)
        ans=re.sub(r'&nbsp','',ans)
        return ans
    return ""

    #用于取出href属性内容
def extracthref(s):
    res=re.search('''href=\"[^"]+"''',s)
    if res:
        return res.group(0)[6:-1].strip()
    return ""

    #用于取出href属性内容
def extracthrefid(s):
    s=extracthref(s)
    if s:
        res=re.search(r"\d+",s)
        if res:
            return res.group(0)
    return "0"

    #用于取出元素内部的xxxx-xx-xx xx:xx:xx格式的时间内容
def extracttime(s):
    s=extracttext(s)
    if s:
        res=re.search(r'\d\d\d\d-\d\d-\d\d\s+\d\d:\d\d:\d\d',s)
        if res:
            print res.group(0)
            return res.group(0)
    return ""
    #取出整数部分
def extractint(s):
    s=extracttext(s)
    if s:
        res=re.search(r'\d+',s)
        if res:
            return res.group(0)
    return ""
    #直接取出整数部分
def extracturlid(s):
    res=re.search(r'\d+.html',s)
    if res:
        return res.group(0)[:-5]
    return ""

def extractstockno(s):
    res=re.search(r',(\d+)',s)
    if res:
        return res.group(1)
    return ""
#######辅助函数#######