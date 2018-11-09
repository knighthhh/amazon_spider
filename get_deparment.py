#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     get_deparment
   Description :
   Author :        hayden_huang
   Date：          2018/11/9 19:51
-------------------------------------------------
"""
import requests
import download
from lxml.etree import HTML
import re
import hashlib
import db


def get_one():
    url = 'https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_pc_0_3015439011_3'
    response = download.get_html(url)
    html = HTML(response.text)
    screenlist = html.xpath('//ul[@id="zg_browseRoot"]/ul/li/a/text()')
    namelist = html.xpath('//ul[@id="zg_browseRoot"]/ul/li/a/@href')
    for item in zip(screenlist,namelist):
        try:
            screenname = item[0]
            url = item[1]
            name = re.search('https://www.amazon.com/(B|b)est-(S|s)ellers-(.*?)/zgbs',item[1]).group(3)
            deparmentid = hashlib.md5(name.encode()).hexdigest()
            type = '1'
        except:
            screenname = item[0]
            url = item[1]
            name = re.search('https://www.amazon.com/(B|b)est-(S|s)ellers/zgbs/(.*?)/', item[1]).group(3)
            deparmentid = hashlib.md5(name.encode()).hexdigest()
            type = '1'
        sql = "insert into onedepa(screenname,url,name,deparmentid,type) values ('%s','%s','%s','%s','%s')"\
                      % (screenname,url,name,deparmentid,type)
        print(sql)
        mysql.save(sql)

def get_two():
    sql = 'select * from onedepa'
    resulsts = mysql.find_all(sql)
    for res in resulsts:
        print(res)
        try:
            pid = str(res[0])
            response = download.get_html(res[5])
            html = HTML(response.text)
            screenlist = html.xpath('//ul[@id="zg_browseRoot"]/ul/ul/li/a/text()')
            namelist = html.xpath('//ul[@id="zg_browseRoot"]/ul/ul/li/a/@href')
            for item in zip(screenlist,namelist):
                screenname = item[0]
                url = item[1]
                name = re.search('https://www.amazon.com/(B|b)est-(S|s)ellers-(.*?)/zgbs/', item[1]).group(3)
                deparmentid = hashlib.md5(name.encode()).hexdigest()
                type = '2'
                sql = "insert into twodepa(pid,screenname,url,name,deparmentid,type) values ('%s','%s','%s','%s','%s','%s')" \
                      % (pid,screenname, url, name, deparmentid, type)
                print(sql)
                mysql.save(sql)
        except:
            pass

def get_three():
    sql = 'select * from twodepa'
    resulsts = mysql.find_all(sql)
    for res in resulsts:
        print(res)
        try:
            pid = str(res[0])
            response = download.get_html(res[6])
            html = HTML(response.text)
            screenlist = html.xpath('//ul[@id="zg_browseRoot"]/ul/ul/ul/li/a/text()')
            namelist = html.xpath('//ul[@id="zg_browseRoot"]/ul/ul/ul/li/a/@href')
            for item in zip(screenlist, namelist):
                screenname = item[0]
                url = item[1]
                name = re.search('https://www.amazon.com/(B|b)est-(S|s)ellers-(.*?)/zgbs/', item[1]).group(3)
                deparmentid = hashlib.md5(name.encode()).hexdigest()
                type = '3'
                sql = "insert into threedepa(pid,screenname,url,name,deparmentid,type) values ('%s','%s','%s','%s','%s','%s')" \
                      % (pid, screenname, url, name, deparmentid, type)
                print(sql)
                mysql.save(sql)
        except:
            pass


if __name__ == '__main__':
    download = download.Download()
    mysql = db.MysqlClient()
    # get_one()
    # get_two()
    get_three()