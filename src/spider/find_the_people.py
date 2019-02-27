# -*- coding: utf-8 -*-

# @Function : find_the_people
# @Time     : 2018/11/28
# @Author   : LiPb
# @Contact  : mocha_lee@qq.com

import sys
sys.path.append("..")
import json
import re
import time
import os
import requests
from public.logger import logging
from public.config import MYSQL_CONFIG
from spider.mysql_base import MysqlHelper


headers = {
        'cookie': '',
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'referer': "https://www.zhihu.com/question/275359100",
        'x-udid': ""
    }
s = requests.session()


def download_avatar(url, save_name):
    resp = s.get(url, headers=headers).content
    if not os.path.exists('../static/img/avatar/'):
        os.makedirs('../static/img/avatar/')
    save_path = '../static/img/avatar/{}'.format(save_name)
    if os.path.exists(save_path):
        return
    with open(save_path, 'wb+') as f:
        f.write(resp)


def update_fetch_time(conn, question_id):
    item = {
        'QuestionId': question_id,
        'UpdateTime': str(int(time.time())),
    }
    result = conn.select('tbl_answer_updatetime_info', f"QuestionId='{question_id}' and IsRemove=0", *('UpdateTime',))
    if len(result) > 0:
        conn.update(table='tbl_answer_updatetime_info', where=f"QuestionId='{question_id}' and IsRemove=0", **item)
    else:
        conn.insert(table='tbl_answer_updatetime_info', **item)


def update_all_data():
    conn = MysqlHelper(logging, host=MYSQL_CONFIG['host'], user=MYSQL_CONFIG['user'], password=MYSQL_CONFIG['psw'],
                       database=MYSQL_CONFIG['db'])

    url = "https://www.zhihu.com/api/v4/questions/275359100/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=20&offset=0&sort_by=default"
    count = 0
    while True:
        try:
            response = s.get(url, headers=headers).json()
        except:
            logging.exception('data fetch error. please contact the author.')
            time.sleep(2)
            continue
        data = response.get('data', [])
        format_data = []

        for one in data:
            author = one.get('author', {}).get('name')
            author_avatar = one.get('author', {}).get('avatar_url')
            avatar_save_name = author_avatar[author_avatar.rfind('/')+1:]
            download_avatar(author_avatar, avatar_save_name)
            author_gender = one.get('author', {}).get('gender')
            author_gender = 2 if author == '匿名用户' else author_gender
            content = one.get('content')
            img_list = re.findall('<figure><noscript><img src="(.*?)" ', content)
            if not img_list:
                img_list = None
            content = re.sub('<figure><noscript><img src="(.*?)</figure>', '<p style="color:#aaa">[这里有一张图片，可以在知乎原答案查看]<p>', content)
            create_time = one.get('created_time')
            update_time = one.get('updated_time')
            _id = one.get('id')
            if not _id:
                continue
            format_data.append({
                'QuestionId': '275359100',
                'AnswerId': _id,
                'AuthorName': author,
                'AuthUrlToken': one.get('author', {}).get('url_token'),
                'AuthorAvatar': avatar_save_name,
                'AuthorGender': author_gender,
                'VoteupCount': one.get('voteup_count', 0),
                'CommentCount': one.get('comment_count', 0),
                'ContentImg': json.dumps(img_list) if img_list else None,
                'TotalContent': content,
                'CreateTime': create_time,
                'UpdateTime': update_time
            })

        for item in format_data:
            try:
                result = conn.select('tbl_couple_answer_info', f"QuestionId='275359100' and AnswerId={item['AnswerId']} and IsRemove=0", *('AuthorName',))
                if len(result) > 0:
                    conn.update(table='tbl_couple_answer_info', where=f"QuestionId='275359100' and AnswerId='{item['AnswerId']}' and IsRemove=0", **item)
                else:
                    conn.insert(table='tbl_couple_answer_info', **item)
            except:
                logging.exception('insert error.')
        count += 20
        paging = response.get('paging')
        if paging.get('is_end'):
            break
        url = paging.get('next')
        print('{} content ok.'.format(count))
    try:
        update_fetch_time(conn, '275359100')
    except:
        logging.exception('insert updatetime error.')
    logging.info('fetch over')


if __name__ == '__main__':
    update_all_data()
