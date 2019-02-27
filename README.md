![](https://github.com/Mocha-L/findtheone/blob/master/pic/findtheone.jpg)  

# [FindTheOne](http://honglingjin.online:520/)

> FindTheOne 知乎红娘小站 是针对知乎大家公布的择偶标准，做的筛选网站（知乎不提供筛选功能好气啊）。在这里可以筛选自己的地域、性别、排序标准等。点击[http://honglingjin.online:520/](http://honglingjin.online:520/)去实例站点查看功能和使用。

## 使用教程

[点击查看教程](https://www.zhihu.com/question/275359100/answer/540772904)

欢迎各位开发者丰富和优化该项目，提交PR。

## 微信交流群

有问题可进群交流或进群联系我。

<img src="https://github.com/Mocha-L/findtheone/blob/master/pic/wecha.jpg" width="250px" />

## 开发

本项目后端主要使用 `Python` + `Flask` ，前端使用 `zhihu`（就是照抄知乎的前端代码进行修改的），数据库是 `Mysql`

### 环境
![](https://img.shields.io/badge/Python-3.6%2B-brightgreen.svg) ![](https://img.shields.io/badge/Flask-1.0.2%2B-brightgreen.svg) ![](https://img.shields.io/badge/Mysql-5.7%2B-brightgreen.svg)

	Python 3.6.*    Mysql 5.7    Flask 1.0.2

### 部署和运行

```
git clone https://github.com/Mocha-L/findtheone.git

pip install -r requirement.txt

python src/web/model.py  # 执行初始化数据库

【重要】copy自己知乎的cookie和x-udid 加入find_the_people.py文件第21行和25行（访问知乎，F12就能看见）

python src/spider/find_the_people.py  # 执行爬虫程序爬取问题答案 也可以将该目录下的auto.sh加入计划任务，定时执行
python src/web/view.py  # 开启网站，默认监听520端口（多浪漫~）
```
### 打赏

觉得有用，请我一杯咖啡。

<img src="https://github.com/Mocha-L/findtheone/blob/master/pic/ali.png" width="230px" /><img src="https://github.com/Mocha-L/findtheone/blob/master/pic/wechat.png" width="230px" />
