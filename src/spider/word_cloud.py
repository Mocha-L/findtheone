# -*- coding: utf-8 -*-
# @Time    : 2019/1/6 17:51
# @Author  : Mocha Lee
# @Email   : 1446684220@qq.com
# @File    : word_cloud.py
# @Software: PyCharm

import jieba
import matplotlib.pyplot as plt
from logger import logging
from wordcloud import WordCloud

from public.config import MYSQL_CONFIG
from spider.mysql_base import MysqlHelper

conn = MysqlHelper(logging, host=MYSQL_CONFIG['host'], user=MYSQL_CONFIG['user'], password=MYSQL_CONFIG['psw'], database=MYSQL_CONFIG['db'])
stopwords = set(list(["然而","这样","另一方面","但是","因此","我们","一个","如果",
                  '它们','具有','人们','可以','这个','这种','不能','因为',
                  '或者','没有','这些','一种','非常','可能','他们','而且',
                  '所有','也许','就是','认为','正如','必须','确定','所以',
                  '任何','发生','甚至','能够','过去','对于','知道','这是',
                  '现在','不同','并且','似乎','那样','其他','什么','不是',
                  '那么','一点','已经','之间','如何','仍然','自己','可以',
             '希望','没有','喜欢','br','要求', '比较', '觉得', '不要', '时候', '不会',
            '虽然', '还是', '很多', '问题', '的话', '最好', 'span', 'class', 'zhimg', 'com', 'zhihu', 'li'
             ]))


def main():
    sql = 'select TotalContent from tbl_couple_answer_info limit 10000'
    result = conn.select_advanced(sql)
    raw_text = ''
    for item in result:
        raw_text += item
    with open('raw_data', 'wb+') as f:
        f.write(raw_text.encode())
    text_cut = " ".join(jieba.cut(raw_text))
    with open('raw_data_cut', 'wb+') as f:
        f.write(text_cut.encode())
    my_cloud = WordCloud(width=1600, height=800, max_words=3000, stopwords=stopwords, font_path="simsun.ttf").generate(text_cut)
    plt.imshow(my_cloud, interpolation='bilinear')
    plt.axis("off")


if __name__ == '__main__':
    main()
