#!/usr/bin/python3
# -*- coding:utf-8 -*-
#
# 作者：X_xxieRiemann
# 链接：http://www.jianshu.com/p/b0991cbc23a4
# 來源：简书
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
#
# pip3 install requests bs4 selenium lxml

import requests, re, time, csv
from bs4 import BeautifulSoup as BS
from selenium import webdriver
#打开网页函数
def open_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36'}
    response = requests.get(url=url, headers=headers)
    response.encoding = 'utf-8'
    html = response.text
    return html
#获取弹幕url中的数字id号

#当requests行不通时，采用selenium的方法。
def sele_get(url):
    print('用 selenium 爬取')
    driver = webdriver.PhantomJS()
    driver.get(url)
    time.sleep(3)
    danmu_id = re.findall(r'cid=(\d+)&', driver.page_source)[0]
    return danmu_id


def get_danmu_id(html, url):
    try:
        soup = BS(html, 'lxml')
        #视频名
        title = soup.select('div.v-title > h1')[0].get_text()
        #投稿人
        author = soup.select('meta[name="author"]')[0]['content']
        #弹幕的网站代码
        try:
            danmu_id = re.findall(r'cid=(\d+)&', html)[0]
        except:
            danmu_id = sele_get(url)
        print('准备抓取得弹幕：', title, author)
        return danmu_id
    except:
        print('视频不见了哟')
        return False
#秒转换成时间
def sec2str(seconds):
    seconds = eval(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    time = "%02d:%02d:%02d" % (h, m, s)
    return time

#csv保存函数
def csv_write(tablelist, path):
    tableheader = ['出现时间', '弹幕模式', '字号', '颜色', '发送时间' ,'弹幕池', '发送者id', 'rowID', '弹幕内容']
    with open(path, 'w', newline='', errors='ignore') as f:
        writer = csv.writer(f)
        writer.writerow(tableheader)
        for row in tablelist:
            writer.writerow(row)

# url = 'http://www.bilibili.com/video//' # 暴走漫画 2k 评论
def get_comments(avid):
    comments = []
    url = 'http://www.bilibili.com/video/%s/' % avid # 古筝 1k

    html = open_url(url)
    danmu_id = get_danmu_id(html, url)
    all_list = []
    if danmu_id:
        danmu_url = 'http://comment.bilibili.com/{}.xml'.format(danmu_id)
        danmu_html = open_url(url=danmu_url)
        soup = BS(danmu_html, 'lxml')
        all_d = soup.select('d')

        in_scrip = False
        for d in all_d:
            #把d标签中P的各个属性分离开
            danmu_list = d['p'].split(',')
            #d.get_text()是弹幕内容
            danmu_list.append(d.get_text())
            danmu_list[0] = sec2str(danmu_list[0])
            danmu_list[4] = time.ctime(eval(danmu_list[4]))
            all_list.append(danmu_list)
            danmu = danmu_list[-1]
            # print(danmu)
            if 'lyric(' in danmu:
                in_scrip = False
            if 'ScriptManager.clearTimer();' in danmu:
                in_scrip = True                
            if type(danmu) == type("a") and not in_scrip and len(danmu) > 1 and not danmu.startswith('[0,') and not danmu.startswith('['):
                comments.append(danmu)
        all_list.sort()
        # csv_write(all_list, './data/%s.csv' % avid)
    print('取得评论: %d' % len(comments))
    return comments

avids = ['av1250357', 'av1387989', 'av285947', 'av113221', 'av810872', 'av404801', 'av24086', 'av1250357', 'av360061', 'av761947', 'av1417519', 'av1039401']
comments = []
for avid in avids:
    comments += get_comments(avid)

with open('./data/bilibili.txt', 'w') as f:
    f.write('\n'.join(set(comments)))
print('总评论: %d' % len(set(comments)))
