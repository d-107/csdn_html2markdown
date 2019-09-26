import requests
from bs4 import BeautifulSoup
import html2markdown
import tomd
import csdn_htmltomd 
import os  #导入模块

def _getimgs(html):
    lists = []
    imghtml = html.select('#content_views > p > img')
    if imghtml is not None:
        for img in imghtml:
            lists.append(img.get('src'))
    return lists

def _getcode(html):
    lists = []
    codehtml = html.select('#content_views > pre > code')
    if codehtml is not None:
        for code in codehtml:
            lists.append(code)
    return lists

def _geturlcontent(url):
    '''
    首先，获取整个页面中博客信息
    标题，时间，内容
    内容中包含 code，img，blockquote，table
    小标题统一为 hx x为数字，对应 ### => h3
    常规文本为 p
    code中内容为 span
    blockquote内容同样为 p
    table 未知
    '''
    strhtml = requests.get(url)
    # print(strhtml.text)
    html = BeautifulSoup(strhtml.text,'html.parser')
    # print(html)

    mdcontent = csdn_htmltomd.getmdcontent(html)
    # print(mdcontent)
    return mdcontent

def wirteDemo1(title,content):
        try:
            #w:覆盖式写入
            #a:追加式写入
            path = './files/wyf'
            file = title + '.md'
            if not os.path.exists(path):
                os.makedirs(path)
            f = open(path + '/' + file, 'w', encoding="utf-8")
            f.write(str(content))
            f.close()
        except Exception:
            print()
            pass

            

# _geturlcontent('https://blog.csdn.net/weixin_44518486/article/details/96482846')

baseurl = 'https://blog.csdn.net/pptsv7'
strhtml = requests.get(baseurl)
#print(strhtml.text)
html = BeautifulSoup(strhtml.text)
#print(html)

urlhtml = html.select('.article-list > .article-item-box > h4 > a')
print(len(urlhtml))

urls = []
for url in urlhtml:
    href = url.get('href')
    urls.append(href)
    # 开始循环获取每个博客内容
    mdcontent = _geturlcontent(href)
    # 写文件(图片先不管)
    wirteDemo1(mdcontent['title'],mdcontent['content'])

print(urls)
