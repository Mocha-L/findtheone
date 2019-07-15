# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuspiderItem(scrapy.Item):
    # define the fields for your item here like:
    QuestionId = scrapy.Field()
    QuestionTitle = scrapy.Field()
    AnswerId = scrapy.Field()
    AuthorName = scrapy.Field()
    AuthUrlToken = scrapy.Field()
    AuthorAvatar = scrapy.Field()
    AuthorGender = scrapy.Field()
    VoteupCount = scrapy.Field()
    CommentCount = scrapy.Field()
    ContentImg = scrapy.Field()
    TotalContent = scrapy.Field()
    CreateTime = scrapy.Field()
    UpdateTime = scrapy.Field()
    Remarks = scrapy.Field()
    IsRemove = scrapy.Field()


class ZhihuspiderImgItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
