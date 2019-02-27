# -*- coding: utf-8 -*-

# @Function : 
# @Time     : 2019/1/8
# @Author   : LiPb (Leon)
# @File     : view.py

from model import Answer, UpdateTime, db, app
from flask import request, render_template, url_for
from datetime import datetime, timedelta
import random
import re
import time


ZAN_WARDS = ['你的赞赏，让我做的更好~', '如果帮到你，请我喝杯咖啡吧~']


@app.template_filter('datetimeformat')
def datetime_format(value):
    timestamp = int(value)
    date_array = datetime.utcfromtimestamp(timestamp) + timedelta(hours=8)
    time_str = date_array.strftime("%Y-%m-%d %H:%M:%S")
    return time_str


@app.route('/comment', methods=['GET'])
def comment():
    return render_template('comment.html')


@app.route('/query', methods=['GET'])
def query_data():
    page = int(request.args.get('page', 1))
    wanna_boy = int(request.args.get('boy', 0))
    wanna_girl = int(request.args.get('girl', 0))
    unknown_person = int(request.args.get('unknown', 0))
    wanna_anonymous = int(request.args.get('anonymous', 0))
    city_name = request.args.get('city', '')
    sort_type = request.args.get('sorttype', '')
    pic_only = int(request.args.get('piconly', 0))

    gender_list = []
    if wanna_boy:
        gender_list.append(1)
    if wanna_girl:
        gender_list.append(0)
    if unknown_person:
        gender_list.append(-1)
    if wanna_anonymous:
        gender_list.append(2)

    filter_list = [Answer.AuthorGender.in_(gender_list), Answer.TotalContent.like('%{}%'.format(city_name)), ]

    if pic_only:
        filter_list.append(Answer.ContentImg.isnot(None))

    order_show = Answer.Id
    if sort_type == 'update':
        order_show = Answer.UpdateTime.desc()
    elif sort_type == 'zan1':
        order_show = Answer.VoteupCount.desc()
    elif sort_type == 'zan2':
        order_show = Answer.VoteupCount
    elif sort_type == 'comment1':
        order_show = Answer.CommentCount.desc()
    elif sort_type == 'comment2':
        order_show = Answer.CommentCount

    ua = request.headers.get('User-Agent')
    mobile = 0
    if ua and re.findall('(iPhone|iPod|Android|ios)'.lower(), ua.lower()):
        mobile = 1

    pagination = Answer.query.filter(*filter_list).order_by(order_show).paginate(page, per_page=5)
    results = pagination.items
    gender_list = [str(one) for one in gender_list]
    query_items = {
        'gender': '、'.join(gender_list).replace('-1', '未知').replace('1', '男').replace('0', '女').replace('2', '匿名'),
        'city': city_name
    }
    if mobile:
        return render_template('data_show_mobile.html', query_items=query_items, results=results, zan_words=random.choice(ZAN_WARDS), pagination=pagination)
    return render_template('data_show.html',query_items=query_items,  results=results, zan_words=random.choice(ZAN_WARDS), pagination=pagination)


@app.route('/', methods=['GET'])
def index():
    boy_count = Answer.query.filter(Answer.AuthorGender.in_([1])).count()
    girl_count = Answer.query.filter(Answer.AuthorGender.in_([0])).count()
    anonymous_count = Answer.query.filter(Answer.AuthorGender.in_([2])).count()
    unknown_person_count = Answer.query.filter(Answer.AuthorGender.in_([-1])).count()
    update_time = UpdateTime.query.filter(UpdateTime.IsRemove == 0, UpdateTime.QuestionId == '275359100').first()
    update_time = update_time.UpdateTime
    all_count = Answer.query.count()
    ua = request.headers.get('User-Agent')
    mobile = 0
    if ua and re.findall('(iPhone|iPod|Android|ios)'.lower(), ua.lower()):
        mobile = 1
    if mobile:
        return render_template(
            'mobile.html',
            update_time=update_time,
            boy_count=boy_count,
            girl_count=girl_count,
            anonymous_count=anonymous_count,
            unknown_person_count=unknown_person_count,
            all_count=all_count
        )
    return render_template(
        'index.html',
        update_time=update_time,
        boy_count=boy_count,
        girl_count=girl_count,
        anonymous_count=anonymous_count,
        unknown_person_count=unknown_person_count,
        all_count=all_count
    )


def url_for_other_page(page):
    # args = request.view_args.copy()
    args = dict(request.args.to_dict().items())
    args['page'] = page
    return url_for(request.endpoint, **args)


def random_background():
    num = random.randint(1, 4)
    return '/static/img/{}.jpg'.format(num)


def random_background_mobile():
    num = random.randint(1, 4)
    return '/static/img/m{}.jpg'.format(num)


if __name__ == '__main__':
    db.create_all()
    app.jinja_env.globals['url_for_other_page'] = url_for_other_page
    app.jinja_env.globals['random_background'] = random_background
    app.jinja_env.globals['random_background_mobile'] = random_background_mobile
    app.run(host='0.0.0.0', port=520, debug=True)
