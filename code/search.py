#这个文件是每次搜索的时候跑的

import json
import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch('http://localhost:9200', basic_auth=('defalt', '123456'))

#这一行是检验es有没有正确连接，连接成功返回True
print(es)

"""
def json_print(string):
    print(json.dumps(string, sort_keys=True, indent=4, separators=(',', ':')))
    return
"""

#搜索方向，默认是"content"
def es_search(keyword,page,direction):
    tmp = "content"
    
    # a = int(input("Search direction (1.title, 2.poet, 3.dynasty, 4.tag, 5.content) : "))
    # for i in range(1,6):
    a = direction
    if a == 1:
        tmp = "name"
    elif a == 2:
        tmp = "poet"
    elif a == 3:
        tmp = "dynasty"
    elif a == 4:
        tmp = "tag"
    elif a == 5:
        tmp = "content"
    #print(tmp)

    

    #搜索内容
    # b = input("Search content : ")
    b = keyword
    query = {
        "query": {
            "match": {
                tmp : b
            }
        },

        #从第0条数据开始
        "from" : 10 * (page - 1),
        #返回10条数据，这个都可以改
        "size" : 10,

        #这是排序，目前是先按照匹配度再按照"popularity"排序
        "sort": [
            {
                "_score" : {
                    "order" : "desc"
                },
                "final_score": {
                    "order" : "desc"
                }
            }
        ]
    }

    result = es.search(index="index_poetry", body=query)
    t = result['hits']['hits']
    tmp = []
    for i in t:
        tmp.append(i['_source'])
    
    return tmp
    #你可以用这行看看会返回什么东西
    # print(type(result))

    #result['hits']['hits']是一个排好序的列表，像下面这样就可以输出一个个只包含原始数据的字典
    # t = result['hits']['hits']
    # for i in t:
    #     print(i['_source'])

# a = es_search('赤壁图')
# for i in a[0]:
#     print(i)







#这是之前测试的时候把它输出到文本文件里的代码，如果报错多半是遇到了txt文件不支持的极个别繁体字
"""
file = open('search_result.txt', mode = 'a')

current_time = datetime.datetime.now()
file.write(str(current_time))
file.write('\n')
file.write(str(tmp))
file.write(" : ")
file.write(str(b))
file.write('\n')

file.write(str(result['hits']['hits']))
file.write('\n\n')

file.close()
"""