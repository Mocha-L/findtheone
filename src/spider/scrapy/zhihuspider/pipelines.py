# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import scrapy
from zhihuspider.public.mysql_base import MysqlHelper
from zhihuspider.public.logger import logging
from zhihuspider.settings import MYSQL_CONFIG
from zhihuspider.items import ZhihuspiderImgItem, ZhihuspiderItem
from scrapy.pipelines.images import ImagesPipeline


conn = MysqlHelper(logging, host=MYSQL_CONFIG['host'], user=MYSQL_CONFIG['user'], password=MYSQL_CONFIG['psw'], database=MYSQL_CONFIG['db'])


class ZhihuspiderPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, ZhihuspiderItem):
            result = conn.select('tbl_couple_answer_info',
                                 f"QuestionId='{item['QuestionId']}' and AnswerId={item['AnswerId']} and IsRemove=0",
                                 *('AuthorName',))
            if len(result) > 0:
                conn.update(table='tbl_couple_answer_info',
                            where=f"QuestionId='{item['QuestionId']}' and AnswerId='{item['AnswerId']}' and IsRemove=0", **item)
            else:
                conn.insert(table='tbl_couple_answer_info', **item)
        return item


class ZhihuspiderImgPipeline(ImagesPipeline):
    headers = {
        'cookie': '',
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'referer': "https://www.zhihu.com/question/275359100",
        'x-udid': ""
    }

    def get_media_requests(self, item, info):
        if isinstance(item, ZhihuspiderImgItem):
            for image_url in item['image_urls']:
                yield scrapy.Request(image_url, headers=self.headers)

    def file_path(self, request, response=None, info=None):
        imgfile = request.url[request.url.rfind('/') + 1:]
        return 'full/{}'.format(imgfile)
