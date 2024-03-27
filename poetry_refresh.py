#这个文件跑一次就好了，第一次是创建，数据库有修改的话再跑

import json
import pymysql
from elasticsearch import Elasticsearch
es = Elasticsearch()

#这一行是检验es有没有正确连接，连接成功返回True
#print(es.ping())

#这里用你自己的数据库连接
conn = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    password = 'root',
    db = 'chinesepoetry',
    charset = 'utf8'
)

#后面直接抄就好，记得在es里装个ik分词器
cursor = conn.cursor()
mappings = {
    "mappings" : {
        "properties" : {
            "name" : {
                "type" : "text",
                "analyzer" : "ik_max_word"
            },
            "poet" : {
                "type" : "text",
                "analyzer" : "ik_max_word"
            },
            "dynasty" : {
                "type" : "text",
                "analyzer" : "ik_max_word"
            },
            "tag" : {
                "type" : "text",
                "analyzer" : "ik_max_word"
            },
            "final_score" : {
                "type" : "float",
            },
            "content" : {
                "type" : "text",
                "analyzer" : "ik_max_word"
            },
            "id" : {
                "type" : "long"
            },
            "authorid" : {
                "type" : "long"
            }
            #如果在数据库加了新东西这里要改
        }
    }
}

# 这一行是删除旧的，第一次不用，以后重置的时候跑
es.indices.delete("index_poetry")

res = es.indices.create(index = 'index_poetry',body = mappings)
sql = 'SELECT * FROM poem WHERE id < 341841'
cursor.execute(sql)
result = cursor.fetchall()
# for i in range(0,341840):
for i in range(0,341793):
    es.index(
        index="index_poetry",
        id=i,
        body={
            "name":result[i][1],
            "poet":result[i][3],
            "dynasty": result[i][2],
            "tag":json.loads(result[i][8]),
            "final_score":result[i][9],
            "content":json.loads(result[i][5]),
            "id":result[i][0],
            "authorid":result[i][4]
            #如果在数据库加了新东西这里也要改
        }
    )
    #因为时间有点长所以加了下面这个显示进程，可以删掉
    if i % 100 == 0:
        print(i)
print("The database is refreshed.")
