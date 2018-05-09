# coding:utf-8
import requests
import re
from bs4 import BeautifulSoup
import traceback
import time
import random
filename = "res.csv"

def GetHtmlText(url):
    text = None
    try:
        r = requests.get(url, headers={'User-Agent': 'Chrome/10'}, timeout=3)
        r.raise_for_status()
        r.encoding = 'utf-8'
        text = r.text
        with open('text.txt','w',encoding='utf-8') as f:
            f.write(text)
        '''
        with open('text.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        '''
        print('get %s succ!' % url)
    except Exception as e:
        traceback.print_exc()
        with open('log.log', 'a') as f:
            f.write('error in %s\n' % url)
    return text

def ParseSubPage(num): # parse sub page with url and title
    content,page_time = [], []
    try:
        # get page content
        url = 'http://tieba.baidu.com/p/'+str(num)
        print('parse sub page: '+str(url))
        text = GetHtmlText(url)
        with open('subtext.txt', 'w', encoding = 'utf-8') as f:
            f.write(text)

        # use re to find content
        pat = r'j_d_post_content  clearfix">            (.*?)</div>'
        res = re.findall(pat, text, re.S | re.M)

        # data clean
        for i in range(len(res)):
            res[i] ,num= re.subn(r'<img(.*?)>', '', res[i].strip())
            res[i], num = re.subn(r'<div(.*?)>', '', res[i].strip())
            res[i], num = re.subn(r'<a(.*?)>', '', res[i].strip())
        content = res

        # get page time
        newpat = r'201[5-8]-[0-9]*-[0-9]*'
        page_time = re.findall(newpat, text)
        page_time.sort()
        page_time = page_time[0]

    except Exception as e:
        traceback.print_exc()
    return content, page_time

def ParsePage(html):
    try:
        res_tr = r'<a rel="noreferrer"  href="/p/(.*?)</a>'
        ready = re.findall(res_tr, html, re.S | re.M)
        page_num = []
        page_title = []

        # get subpage url and its title
        for i in ready:
            page_num.append(i[:10])
            pat = r'title="(.*?)"'
            res_name = re.findall(pat, i, re.S | re.M)
            page_title.append(res_name)

        # get subpage content
        page_content = []
        for i in range(len(page_num)):
            #print(page_num[i], page_title[i])
            content, subpage_time = ParseSubPage(page_num[i])

            infoList = [page_title[i], content, subpage_time]
            PrintList(infoList)
            #time.sleep(random.random()*8)

    except Exception as e:
        traceback.print_exc()

def PrintList(ilt):
    with open(filename, 'a+', encoding='utf-8') as f:
        title = ilt[0]
        content = ilt[1]
        time = ilt[2]
        print('get title: ' + str(title))
        print('get time: ' + str(time))
        print('get content: ' + str(content))

        if len(time)==0:
            time='NULL'
        if len(content)==0:
            content=[['content is empty!']]
        f.write(time + ',')
        f.write(title[0] + ',')
        for j in range(len(content)):
            f.write(str(content[j]) + str(', '))
        f.write('\n')

def wmain():
    infoList = []
    print("--spider for tieba.baidu.com getting off...")
    '''
    with open('res.csv', 'w') as f:
        f.write('time,title,content\n')
    '''
    indexPerPage=50
    TotalPageNum = 250
    for i in range(60, TotalPageNum):
        if (i-60)%50==0:
            filename = "res" + str(int((i-60)/50+1))+".csv"
        try:
            url = "http://tieba.baidu.com/f?kw=ofo&ie=utf-8&pn=" + str(i*indexPerPage)
            html = GetHtmlText(url)
            infoList = ParsePage(html)
            print("--spider page " + str(i+1) + " succ!")

            #time.sleep(5*random.random())
        except Exception as e:
            traceback.print_exc()
            continue


# 打印通知：“爬虫开始”->构造url->得到html，处理->输出结果，打印log

wmain()