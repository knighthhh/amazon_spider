import datetime
import json
import threading
from time import sleep
import multiprocessing
import config
import re
import time
import redis
import html as HT
from lxml import etree
from lxml.etree import HTML
from download import Download
from db import MongoClient, MysqlClient, RedisClient


class Scheduler(object):
    def __init__(self):
        self.download = Download()
        # self.db = MysqlClient()
        # self.redisClient = RedisClient()

    def run(self):
        self.get_kw()

    def get_kw(self):
        url = 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=iphone'
        response = self.download.get_html(url)
        if response is not None:
            html = HTML(response.text)
            # titles = html.xpath('//div[@class="a-row a-spacing-small"]//a/h2/text()')
            urls = html.xpath('//div[@class="a-row a-spacing-small"]//a/@href')
            for url in urls:
                if url[0:4] == 'http':
                    url = url
                else:
                    url = 'https://www.amazon.com' + url
                print(url)
                detail_response = self.download.get_html(url)
                detail_html = HTML(detail_response.text)
                title = detail_html.xpath('string(//h1[@id="title"])').strip()
                price = detail_html.xpath('string(//span[@id="priceblock_ourprice"])').replace(',', '').replace('$', '')
                color = detail_html.xpath('string(//div[@id="variation_color_name"]//span)').strip()
                size = detail_html.xpath('string(//div[@id="variation_size_name"]//span)').strip()
                commentCount = detail_html.xpath('string(//span[@id="acrCustomerReviewText"])').split(' ')[0].replace(',', '')
                commentRating = detail_html.xpath('string(//a[@class="a-popover-trigger a-declarative"]/i/span)').split(' ')[0]

                #匹配图片
                imageUrls = []
                img_res = re.search("var data = {};.*?var obj = jQuery.parseJSON\('(.*?)'\);", detail_response.text, re.S)
                img_obj = json.loads(img_res.group(1))
                try:
                    key_one = list(img_obj['colorImages'].keys())[0]
                    for data in img_obj['colorImages'][key_one]:
                        imageUrls.append(data['large'])
                except:
                    pass

                obj = {
                    'title': title,
                    'price': price,
                    'color': color,
                    'size': size,
                    'commentCount': commentCount,
                    'commentRating': commentRating,
                    'imageUrls': imageUrls,
                }
                print(obj)
