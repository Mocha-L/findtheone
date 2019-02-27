# -*- coding: utf-8 -*-

# @Function : 
# @Time     : 2019/1/8
# @Author   : LiPb (Leon)

# @File     : model.py

import sys
sys.path.append("..")
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, Index, text
from public.config import MYSQL_CONFIG

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:3306/{}?charset=utf8'.format(MYSQL_CONFIG['user'], MYSQL_CONFIG['psw'], MYSQL_CONFIG['host'], MYSQL_CONFIG['db'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
# Base = declarative_base()  # 创建对象的基类


class Answer(db.Model):

    __tablename__ = 'tbl_couple_answer_info'

    # 表的结构:
    Id = Column(Integer, primary_key=True, autoincrement=True)
    # name = Column(String(32), index=True, nullable=False, default='xx')  # index指定是否是索引，nullable是否能为空
    QuestionId = Column(String(32), nullable=False)
    AnswerId = Column(String(32), nullable=False)
    AuthorName = Column(String(255), nullable=True)
    AuthUrlToken = Column(String(255), nullable=True)
    AuthorAvatar = Column(String(255), nullable=True)
    AuthorGender = Column(Integer, nullable=False)
    VoteupCount = Column(Integer, nullable=False)
    CommentCount = Column(Integer, nullable=False)
    ContentImg = Column(Text, nullable=True)
    TotalContent = Column(Text, nullable=False)
    CreateTime = Column(Integer, nullable=False, server_default=text('0'))
    UpdateTime = Column(Integer, nullable=False, server_default=text('0'))
    Remarks = Column(String(255), nullable=True)
    IsRemove = Column(Integer, nullable=False, server_default=text('0'))

    __table_args__ = (Index('ix_name_gender', 'AuthorName', 'AuthorGender', 'UpdateTime', 'IsRemove'),)  # 创建普通索引，索引名为ix_id_name


class UpdateTime(db.Model):

    __tablename__ = 'tbl_answer_updatetime_info'

    # 表的结构:
    Id = Column(Integer, primary_key=True, autoincrement=True)
    # name = Column(String(32), index=True, nullable=False, default='xx')  # index指定是否是索引，nullable是否能为空
    QuestionId = Column(String(32), nullable=False)
    UpdateTime = Column(Integer, nullable=False, server_default=text('0'))
    Remarks = Column(String(255), nullable=True)
    IsRemove = Column(Integer, nullable=False, server_default=text('0'))


# def init_db():
#     """
#     根据类创建数据库表
#     :return:
#     """
#     # 初始化数据库连接:
#     engine = create_engine("mysql+pymysql://leon:19931029@127.0.0.1:3306/zhihucouple?charset=utf8", max_overflow=0,  # 超过连接池大小外最多创建的连接
#         pool_size=5,  # 连接池大小
#         pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
#         pool_recycle=-1)  # 多久之后对线程池中的线程进行一次连接的回收（重置）)
#
#     Base.metadata.create_all(engine)  # 找到所有继承了Base的类，按照其结构建表


if __name__ == '__main__':
    db.create_all()
