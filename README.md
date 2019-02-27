# FindTheOne 知乎红娘小站

![](http://honglingjin.online:520/static/img/3.jpg)  

# [FindTheOne](http://honglingjin.online:520/)

> FindTheOne 知乎红娘小站 是针对知乎大家公布的择偶标准，做的筛选网站（知乎不提供筛选功能好气啊）。在这里可以筛选自己的地域、性别、排序标准等。

## 使用教程

[点击查看教程](https://www.zhihu.com/question/275359100/answer/540772904)

## 微信交流群



## 开发

本项目后端主要使用 `Python` + `Flask` ，前端使用 `zhihu`（就是照抄知乎的前端代码进行修改的），数据库是 `Mysql`

### 环境
![](https://img.shields.io/badge/Python-3.6%2B-brightgreen.svg) ![](https://img.shields.io/badge/Flask%2B-brightgreen.svg) ![](https://img.shields.io/badge/Mysql-5.7%2B-brightgreen.svg)

	Python 3.6.*
  Mysql 5.7
  Flask

### 编译

```
git clone https://github.com/proxyee-down-org/proxyee-down.git
cd proxyee-down/front
#build html
npm install
npm run build
cd ../main
mvn clean package -Pprd
```

### 运行
```
java -jar proxyee-down-main.jar
```
