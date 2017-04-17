# -*- coding: utf-8 -*-
# !/usr/bin/env python
#coding=gbk

from lxml import etree
import requests
import pymysql
import matplotlib.pyplot as plt
import ch
ch.set_ch()
from pylab import *
import numpy as np

# 连接mysql数据库
conn = pymysql.connect(host = '127.0.0.1', user = 'root', password = '123456', db = 'douban', charset = 'utf8')
cur = conn.cursor()
cur.execute('SELECT VERSION()')
cur.execute('use douban;')


def get_page(_pageID):
    url = 'https://movie.douban.com/top250?start={}&filter='.format(_pageID)

    html = requests.get(url).content.decode('utf-8')

    selector = etree.HTML(html)

    content = selector.xpath('//div[@class="info"]/div[@class="bd"]/p/text()')
    ##jerry note: list encode to utf-8 str
    # content = str( u''.join(content).encode('utf-8') )
    # print(content)
    print "\n====PAGE {}=====".format(_pageID/25 + 1)
    global cnt
    for i in content[1::2]:

        #current line is null, skip, continue
        if i.strip().replace('\n', '') == '':
            # print '--------no line-------'
            continue

        cnt += 1
        # print '----new line----'
        print u''.join(i.strip().replace('\n', '')).encode('utf-8')
        i = i.strip().replace('\n', '').strip().split('/')
        #movies class's
        i = i[len(i) - 1].strip()
        # print i
        keys = i.split(' ')
        # print keys
        for key in keys:
            if key == '':
                continue
            if key not in douban.keys():
                douban[key] = 1
            else:
                douban[key] += 1 
    # error page
    if cnt % 25 != 0:
        print "\n=======cnt is not 25's=====page", _pageID / 25 + 1

## create db
# create douban

## create table
# create table douban(
#     id INT NOT NULL AUTO_INCREMENT,
#     class VARCHAR(100) NOT NULL,
#     count INT NOT NULL,
#     PRIMARY KEY( id )
#     )ENGINE=InnoDB DEFAULT CHARSET=utf8;

##drop table tablename

def save_mysql():
    cur.execute('truncate table douban')
    print(douban)
    for key in douban:
        print key, douban[key]
        if key != '':
            try:
                # 'insert into douban (class, count) values("同性",8);'
                sql = 'insert into douban (class, count) values('  + '"' + key + '"' + ',' + str(douban[key]) + ');'
                print sql
                cur.execute(sql)
                conn.commit()
            except:
                print '插入失败'
                conn.rollback()


def pyplot_show():
    print "\n====in function: pyplot_show==="
    try:
        sql = 'select * from douban;'
        cur.execute(sql)
        rows = cur.fetchall()
        count = []
        category = []

        for row in rows:
            count.append(int(row[2]))
            category.append(row[1])
    except:
        print("Error: unable to fecth data")
    print(count)
    y_pos = np.arange(len(category))
    print(y_pos)
    print(category)
    colors = np.random.rand(len(count))
    # plt.barh()
    plt.barh(y_pos, count, align='center', alpha=0.7)
    plt.yticks(y_pos, category)
    for count, y_pos in zip(count, y_pos):
        plt.text(count+4, y_pos, count,  horizontalalignment='center', verticalalignment='center', weight='bold')
    plt.ylim(+27.0, -1.0)
    plt.title(u'豆瓣电影250')
    plt.ylabel(u'电影分类')
    plt.subplots_adjust(bottom = 0.15)
    plt.xlabel(u'分类出现次数')
    plt.savefig('douban.png')


if __name__ == '__main__':
    douban = {}
    cnt = 0
    # get_page(225)
    for i in range(0, 250, 25):
        get_page(i)
    # douban = {u'\u540c\u6027': 8, u'\u7eaa\u5f55\u7247': 4, u'\u5bb6\u5ead': 25, u'\u6b66\u4fa0': 3, u'\u7231\u60c5': 63, u'\u60ac\u7591': 32, u'\u513f\u7ae5': 7, u'\u707e\u96be': 1, u'\u52a8\u4f5c': 36, u'\u559c\u5267': 49, u'\u5267\u60c5': 193, u'\u52a8\u753b': 31, u'\u6218\u4e89': 17, u'\u60ca\u609a': 29, u'\u79d1\u5e7b': 24, u'\u97f3\u4e50': 7, u'\u4f20\u8bb0': 12, u'\u897f\u90e8': 5, u'\u8fd0\u52a8': 1, u'\u5192\u9669': 45, u'\u72af\u7f6a': 48, u'\u5386\u53f2': 9, u'\u6050\u6016': 2, u'\u53e4\u88c5': 7, u'\u5947\u5e7b': 36, u'\u6b4c\u821e': 5, u'\u60c5\u8272': 1}
    print 'cnt =', cnt
    for key in douban.keys():
        print key, douban[key]
    save_mysql()
    pyplot_show()
    cur.close()
    conn.close()
