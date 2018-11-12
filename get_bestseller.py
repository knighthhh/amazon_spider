#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     get_bestseller
   Description :
   Author :        hayden_huang
   Date：          2018/11/11 21:20
-------------------------------------------------
"""

import datetime
import json
import threading
from time import sleep
import multiprocessing
import config
import re
import time
import redis
from lxml import etree
import hashlib
from lxml.etree import HTML
from lxml import etree
import math
from download import Download
from db import MongoClient, MysqlClient, RedisClient

class Bestseller(object):
    def __init__(self):
        self.download = Download()
        self.mysql = MysqlClient()

    def start(self):
        res1 = self.get_url('onedepa')
        res2 = self.get_url('twodepa')
        res3 = self.get_url('threedepa')

        self.get_html(res1)
        # self.get_html(res2)
        # self.get_html(res3)

    def get_url(self,typename):
        sql = "select * from %s"%(typename)
        results = self.mysql.find_all(sql)
        return results

    def get_html(self,results):
        for res in results:
            url = res[5]
            typeid= res[0]
            temp_url_lit = []
            url_one = url
            page2_replace = re.search('https://www.amazon.com.*?ref=zg_bs_(.*?/\d+-\d+-\d+)', url).group(1)
            url_tow = url.replace(page2_replace,'pg_2?&pg=2')
            temp_url_lit.append(url_one)
            temp_url_lit.append(url_tow)
            for url in temp_url_lit:
                print(url)
                response = self.download.get_html(url)
                if response:
                    html = HTML(response.text)
                    url_list = html.xpath('//div[@id="zg-center-div"]/ol/li//a[@class="a-link-normal a-text-normal"]/@href')
                    for detail_url in url_list:
                        spider_url = 'https://www.amazon.com' + detail_url
                        print(spider_url)
                        detail_response = self.download.get_html(spider_url)
                        if detail_response:
                            detail_html = HTML(detail_response.text)
                            sellrank = re.search('https://www.amazon.com/.*?/dp/.*?ref=.*?_(\d+)/\d+-\d+-\d+\?',spider_url).group(1)
                            print('sellrank:'+ sellrank)

                            product_id = hashlib.md5(detail_url.encode()).hexdigest()
                            title = detail_html.xpath('string(//h1[@id="title"])').strip()
                            price = detail_html.xpath('string(//span[@id="priceblock_ourprice"])').replace(',', '').replace('$', '')
                            color = detail_html.xpath('string(//div[@id="variation_color_name"]//span)').strip()
                            size = detail_html.xpath('string(//div[@id="variation_size_name"]//span)').strip()
                            commentCount = detail_html.xpath('string(//span[@id="acrCustomerReviewText"])').split(' ')[0].replace(',', '')
                            commentRating = detail_html.xpath('string(//a[@class="a-popover-trigger a-declarative"]/i/span)').split(' ')[0]
                            crawled_timestamp = int(time.time())
                            crawled_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                            # 编号
                            try:
                                asin = re.search('https://www.amazon.com/.*?/dp/(.*?)/ref=.*?', spider_url).group(1)
                            except:
                                asin = None

                            # 类目排名
                            rank1 = None
                            rank2 = None
                            # try:
                            #     category_res1 = re.search('.*?productDetails_detailBullets_sections1.*?Best Sellers Rank.*?<span>.*?(<span>.*?</span>)',detail_response.text, re.S)
                            #     category_res2 = re.search('.*?productDetails_detailBullets_sections1.*?Best Sellers Rank.*?<span>.*?<span>.*?</span>.*?(<span>.*?</span>).*?</span>', detail_response.text, re.S)
                            #     if category_res1:
                            #         # rank_search = re.search('.*?#(.*?)in.*?', category_res1.group(1))
                            #         # if rank_search:
                            #         #     rank1 = rank_search.group(1)
                            #         # else:
                            #         #     rank1 = None
                            #         # print(rank1)
                            #         html = HTML(category_res1.group(1))
                            #         list_res = html.xpath('//text()')
                            #         rank1 = ''.join(list_res)
                            #     if category_res2:
                            #         html = HTML(category_res2.group(1))
                            #         list_res = html.xpath('//text()')
                            #         rank2 = ''.join(list_res)
                            # except:
                            #     rank1 = None
                            #     rank2 = None
                            # 图片信息入库
                            try:
                                imageUrls = []
                                img_res = re.search("var data = {};.*?var obj = jQuery.parseJSON\('(.*?)'\);",
                                                    detail_response.text,
                                                    re.S)
                                img_obj = json.loads(img_res.group(1))
                                key_one = list(img_obj['colorImages'].keys())[0]
                                for data in img_obj['colorImages'][key_one]:
                                    imageUrls.append(data['large'])
                                for img in imageUrls:
                                    img_id = hashlib.md5(img.encode()).hexdigest()
                                    img_url = img
                                    sql = "insert into image(product_id,img_id,img_url,crawled_timestamp,crawled_time) values ('%s','%s','%s','%s','%s')" \
                                          % (asin, img_id, img_url, crawled_timestamp, crawled_time) \
                                          + "ON DUPLICATE KEY UPDATE crawled_timestamp='%s',crawled_time='%s'" % (crawled_timestamp, crawled_time)
                                    print(sql)
                                    self.mysql.save(sql)
                            except:
                                pass

                            # 跟卖信息入库
                            have_follow_sale = '0'
                            follow_sale_num = 0
                            follow_sale_str = detail_html.xpath('string(//div[@id="olpPocs_feature_div"]/div/span)')
                            if follow_sale_str != '':
                                have_follow_sale = '1'
                                follow_sale_num = re.search('\((\d+)\)', follow_sale_str).group(1)

                            follow_sale_url = detail_html.xpath('string(//div[@id="olpPocs_feature_div"]/div/span/a/@href)')
                            if follow_sale_url[0:4] == 'http':
                                follow_sale_url = follow_sale_url
                            else:
                                follow_sale_url = 'https://www.amazon.com' + follow_sale_url + '&startIndex={startIndex}'
                            follow_response = self.get_follow_sale(follow_sale_url, follow_sale_num)
                            for item in follow_response:
                                follow_sale_id = item['follow_sale_id']
                                price = item['price']
                                seller = item['seller']
                                type = item['type']
                                sql = "insert into follow_sale(product_id,follow_sale_id,price,seller,type,crawled_timestamp,crawled_time) values ('%s','%s','%s','%s','%s','%s','%s')" \
                                      % (asin, follow_sale_id, price, seller, type, crawled_timestamp, crawled_time) \
                                      + "ON DUPLICATE KEY UPDATE crawled_timestamp='%s',crawled_time='%s'" % (crawled_timestamp, crawled_time)
                                print(sql)
                                self.mysql.save(sql)

                            # 商品信息入库
                            sql = "insert into bestseller(typeid,sellrank,product_id,title,url,price,color,size,commentCount,commentRating,have_follow_sale,follow_sale_num,asin,rank1,rank2,crawled_timestamp,crawled_time) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                                  % (typeid,sellrank,product_id,title,url,price,color,size,commentCount,commentRating,have_follow_sale,follow_sale_num,asin,rank1,rank2,crawled_timestamp,crawled_time) \
                                  + "ON DUPLICATE KEY UPDATE sellrank='%s',title='%s', url='%s', price='%s',commentCount='%s',crawled_timestamp='%s',crawled_time='%s',follow_sale_num='%s'" % (
                                    sellrank, title, spider_url, price, commentCount, crawled_timestamp, crawled_time,follow_sale_num)
                            print(sql)
                            self.mysql.save(sql)

    def get_follow_sale(self, url, follow_sale_num):
        if follow_sale_num == 0:
            return []
        if int(follow_sale_num) > 10:
            pageNum = math.ceil(int(follow_sale_num)/10)
        else:
            pageNum = 1

        item_list = []
        for page in range(0, pageNum):
            startIndex = page * 10
            url = url.format(startIndex=startIndex)
            print(url)
            follow_response = self.download.get_html(url)
            if follow_response is None:
                return []
            follow_html = HTML(follow_response.text)

            html_list = follow_html.xpath('//div[@class="a-row a-spacing-mini olpOffer"]')
            for html in html_list:
                html = etree.tostring(html).decode()
                html = HTML(html)
                price = html.xpath('string(//div[@class="a-column a-span2 olpPriceColumn"]/span)').strip().replace('$','')
                seller = html.xpath('string(//h3/span)').strip()
                FBA = html.xpath('string(//div[@class="olpBadge"])')
                type = 'FBM'
                if FBA != '':
                    type = 'FBA'
                follow_sale_id = hashlib.md5((seller+price+type).encode()).hexdigest()
                obj = {
                    'follow_sale_id': follow_sale_id,
                    'price': price,
                    'seller': seller,
                    'type': type
                }
                print(obj)
                item_list.append(obj)
        return item_list