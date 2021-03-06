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
import get_bestseller
from download import Download
from db import MongoClient, MysqlClient, RedisClient


class Scheduler(object):
    def __init__(self):
        self.download = Download()
        self.db = MysqlClient()
        # self.redisClient = RedisClient()

    def run(self):
        bestseller = get_bestseller.Bestseller()
        bestseller.start()
        # for i in range(1,11):
        #     self.get_kw('apple',str(i))

    def get_kw(self,kw, page):
        url = 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords={kw}&page={page}'.format(kw=kw,page=page)
        print(url)
        response = self.download.get_html(url)
        if response is not None:
            html = HTML(response.text)
            # titles = html.xpath('//div[@class="a-row a-spacing-small"]//a/h2/text()')
            urls = html.xpath('//div[@class="a-row a-spacing-small"]//a/@href')
            for url in urls:
                if url[:3] == '/gp':
                    url = 'https://www.amazon.com' + url
                detail_response = self.download.get_html(url)
                try:
                    url = re.search('<link rel="canonical" href="(.*?)"',detail_response.text).group(1)
                except:
                    url = url

                detail_html = HTML(detail_response.text)
                product_id = hashlib.md5(url.encode()).hexdigest()
                title = detail_html.xpath('string(//h1[@id="title"])').strip()
                price = detail_html.xpath('string(//span[@id="priceblock_ourprice"])').replace(',', '').replace('$', '')
                if price == '':
                    price = 0
                color = detail_html.xpath('string(//div[@id="variation_color_name"]//span)').strip()
                size = detail_html.xpath('string(//div[@id="variation_size_name"]//span)').strip()
                commentCount = detail_html.xpath('string(//span[@id="acrCustomerReviewText"])').split(' ')[0].replace(',', '')
                if commentCount == '':
                    commentCount = 0
                commentRating = detail_html.xpath('string(//a[@class="a-popover-trigger a-declarative"]/i/span)').split(' ')[0]
                if commentRating == '':
                    commentRating = 0
                crawled_timestamp = int(time.time())
                crawled_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                crawled_date = time.strftime("%Y-%m-%d", time.localtime())
                keywordtype = kw

                #编号
                try:
                    asin = re.search('.*?productDetails_detailBullets_sections1.*?ASIN.*?<td class="a-size-base">(.*?)</td>',detail_response.text,re.S).group(1).strip()
                except:
                    asin = None
                #类目排名
                try:
                    category_res1 = re.search('.*?productDetails_detailBullets_sections1.*?Best Sellers Rank.*?<span>.*?(<span>.*?</span>)',detail_response.text,re.S)
                    category_res2 = re.search('.*?productDetails_detailBullets_sections1.*?Best Sellers Rank.*?<span>.*?<span>.*?</span>.*?(<span>.*?</span>).*?</span>',detail_response.text,re.S)
                    if category_res1:
                        # rank_search = re.search('.*?#(.*?)in.*?', category_res1.group(1))
                        # if rank_search:
                        #     rank1 = rank_search.group(1)
                        # else:
                        #     rank1 = None
                        # print(rank1)
                        html = HTML(category_res1.group(1))
                        list_res = html.xpath('//text()')
                        rank1 = ''.join(list_res)
                    if category_res2:
                        html = HTML(category_res2.group(1))
                        list_res = html.xpath('//text()')
                        rank2 = ''.join(list_res)
                except:
                    rank1 = None
                    rank2 = None

                #图片信息入库
                try:
                    imageUrls = []
                    img_res = re.search("var data = {};.*?var obj = jQuery.parseJSON\('(.*?)'\);", detail_response.text,
                                        re.S)
                    img_obj = json.loads(img_res.group(1))
                    key_one = list(img_obj['colorImages'].keys())[0]
                    for data in img_obj['colorImages'][key_one]:
                        imageUrls.append(data['large'])

                    for img in imageUrls:
                        img_id =  hashlib.md5(img.encode()).hexdigest()
                        img_url = img
                        sql = "insert into image(product_id,img_id,img_url,crawled_timestamp,crawled_time) values ('%s','%s','%s','%s','%s')" \
                              % (product_id,img_id,img_url,crawled_timestamp,crawled_time) \
                              + "ON DUPLICATE KEY UPDATE crawled_timestamp='%s',crawled_time='%s'" % (crawled_timestamp, crawled_time)
                        print(sql)
                        self.db.save(sql)
                except:
                    pass

                #跟卖信息入库
                have_follow_sale = '0'
                follow_sale_num = 0
                follow_sale_str = detail_html.xpath('string(//div[@id="olp_feature_div"]/div/span)')
                if follow_sale_str != '':
                    have_follow_sale = '1'
                    follow_sale_num = re.search('\((\d+)\)',follow_sale_str).group(1)

                follow_sale_url = detail_html.xpath('string(//div[@id="olp_feature_div"]/div/span/a/@href)')
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
                          % (product_id,follow_sale_id,price,seller,type,crawled_timestamp,crawled_time) \
                          + "ON DUPLICATE KEY UPDATE crawled_timestamp='%s',crawled_time='%s'" % (crawled_timestamp, crawled_time)
                    print(sql)
                    self.db.save(sql)

                #商品信息入库
                obj = {
                    'product_id': product_id,
                    'title': title,
                    'url': url,
                    'price': price,
                    'color': color,
                    'size': size,
                    'commentCount': commentCount,
                    'commentRating': commentRating,
                    # 'imageUrls': imageUrls,
                    'crawled_timestamp': crawled_timestamp,
                    'crawled_time': crawled_time,
                    'have_follow_sale': have_follow_sale,
                    'follow_sale_num': follow_sale_num,
                }
                print(obj)
                sql = "insert into keyword_res(product_id,title,url,price,color,size,commentCount,commentRating,have_follow_sale,follow_sale_num,asin,rank1,rank2,crawled_timestamp,crawled_time,crawled_date,keywordtype) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
                      % (product_id, title, url, price, color, size, commentCount, commentRating,have_follow_sale,follow_sale_num,asin,rank1,rank2, crawled_timestamp, crawled_time,crawled_date,keywordtype)\
                      + "ON DUPLICATE KEY UPDATE title='%s', url='%s', price='%s',commentCount='%s',crawled_timestamp='%s',crawled_time='%s',crawled_date='%s'"%(title,url,price,commentCount,crawled_timestamp,crawled_time,crawled_date)
                print(sql)
                self.db.save(sql)

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

