# 注意事项
**本文件夹中所有代码的路径默认均以本文件夹为根目录，请注意修改！！！**
**进行操作前请提前备份好已爬好的数据**

# 项目结构
-poet/
 -async_scrapy_poet.py
 -poet.js
-poem
 -poetry/
  -35 json files
 -async_scrapy_poem_link.py
 -async_scrapy_poem_detail.py
-verses/
 -async_scrapy_verses.py
 -verses.json
-famous_verses/
 -async_scrapy_famous_verses.py
 -famous_verses.json

# 运行指南
 先运行async_scrapy_poet.py获取诗人信息以及诗人对应的诗歌界面，再运行async_scrapy_poem_link.py获取每首诗歌详细链接，最后运行async_scrapy_poem_detail.py获取诗歌详细信息
 async_scrapy_famous_verses.py和async_scrapy_verses.py无依赖关系