# python 爬取豆瓣电影top250提取电影分类进行数据分析
转载博客：https://segmentfault.com/a/1190000005920679
我的博客：mysql，pymysql安装配置
	http://www.cnblogs.com/johnleo/p/python_script_douban_top250movies.html

系统：OSX EI 10.11


## 知识点
- python 爬虫requests包，lxml.etree包, 网页前端
- 网页字符编码,编码集Ascall, UTF-8, GBK，unicode--encode-->str, str--decode-->unicode
- mysql，pymysql
	mac mysql 安装，启动，*登录用户*，停止；
	pymysql安装，插入，查询等操作
- matplotlib.pyplot绘图
	中文字符集，乱码问题


## 使用
- 开启mysql服务，创建数据库
- python demo.py